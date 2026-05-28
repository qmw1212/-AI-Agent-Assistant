"""
Memory Management Module — SQLite Persistent Memory
Stores conversations, messages, and user info in agent_memory.db
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, date


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent_memory.db")


class PersistentMemory:
    """SQLite-backed persistent memory for conversations and user info."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    title     TEXT    NOT NULL DEFAULT 'New Chat',
                    created_at TEXT   NOT NULL,
                    updated_at TEXT   NOT NULL
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role            TEXT    NOT NULL,
                    content         TEXT    NOT NULL,
                    timestamp       TEXT    NOT NULL,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS user_memory (
                    key        TEXT PRIMARY KEY,
                    value      TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
            """)

    # ── Conversation CRUD ─────────────────────────────────────────────────────

    def create_conversation(self, title: str = "New Chat") -> int:
        now = datetime.now().isoformat()
        with self._conn() as conn:
            cur = conn.execute(
                "INSERT INTO conversations (title, created_at, updated_at) VALUES (?, ?, ?)",
                (title, now, now)
            )
            return cur.lastrowid

    def update_title(self, conv_id: int, title: str):
        now = datetime.now().isoformat()
        with self._conn() as conn:
            conn.execute(
                "UPDATE conversations SET title=?, updated_at=? WHERE id=?",
                (title[:40], now, conv_id)
            )

    def delete_conversation(self, conv_id: int):
        with self._conn() as conn:
            conn.execute("DELETE FROM conversations WHERE id=?", (conv_id,))

    def list_conversations(self) -> List[Dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id, title, created_at, updated_at FROM conversations ORDER BY updated_at DESC"
            ).fetchall()
        return [dict(r) for r in rows]

    def get_conversation(self, conv_id: int) -> Optional[Dict]:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT id, title, created_at, updated_at FROM conversations WHERE id=?",
                (conv_id,)
            ).fetchone()
        return dict(row) if row else None

    # ── Messages ──────────────────────────────────────────────────────────────

    def add_message(self, conv_id: int, role: str, content: str):
        now = datetime.now().isoformat()
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO messages (conversation_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                (conv_id, role, content, now)
            )
            conn.execute(
                "UPDATE conversations SET updated_at=? WHERE id=?", (now, conv_id)
            )

    def get_messages(self, conv_id: int) -> List[Dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT role, content, timestamp FROM messages WHERE conversation_id=? ORDER BY id",
                (conv_id,)
            ).fetchall()
        return [dict(r) for r in rows]

    def get_recent_messages_for_llm(self, conv_id: int, limit: int = 10) -> List[Dict[str, str]]:
        """Return last N messages as {role, content} dicts for LLM context."""
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT role, content FROM messages WHERE conversation_id=? ORDER BY id DESC LIMIT ?",
                (conv_id, limit)
            ).fetchall()
        return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]

    # ── User Memory ───────────────────────────────────────────────────────────

    def save_user_info(self, key: str, value: str):
        now = datetime.now().isoformat()
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO user_memory (key, value, updated_at) VALUES (?, ?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
                (key, value, now)
            )

    def get_user_info(self, key: str) -> Optional[str]:
        with self._conn() as conn:
            row = conn.execute("SELECT value FROM user_memory WHERE key=?", (key,)).fetchone()
        return row["value"] if row else None

    def get_all_user_info(self) -> Dict[str, str]:
        with self._conn() as conn:
            rows = conn.execute("SELECT key, value FROM user_memory").fetchall()
        return {r["key"]: r["value"] for r in rows}

    def clear_user_info(self):
        with self._conn() as conn:
            conn.execute("DELETE FROM user_memory")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def get_context_summary(self) -> str:
        """Human-readable memory summary for sidebar display."""
        info = self.get_all_user_info()
        if not info:
            return "No user info stored yet."
        lines = ["**Remembered about you:**"]
        labels = {"name": "Name", "likes": "Likes", "study_place": "Studies at",
                  "major": "Major", "study": "Studies"}
        for key, value in info.items():
            label = labels.get(key, key.capitalize())
            lines.append(f"- {label}: {value}")
        return "\n".join(lines)

    def group_conversations_by_date(self) -> Dict[str, List[Dict]]:
        """Group conversation list into Today / Yesterday / Earlier."""
        convs = self.list_conversations()
        today = date.today().isoformat()
        from datetime import timedelta
        yesterday = (date.today() - timedelta(days=1)).isoformat()

        groups: Dict[str, List[Dict]] = {"今天": [], "昨天": [], "更早": []}
        for c in convs:
            day = c["updated_at"][:10]
            if day == today:
                groups["今天"].append(c)
            elif day == yesterday:
                groups["昨天"].append(c)
            else:
                groups["更早"].append(c)
        return groups


class SessionMemory:
    """Thin static-method wrapper kept for backward compat with app.py call sites."""

    @staticmethod
    def initialize_session_state(st):
        if "db" not in st.session_state:
            st.session_state.db = PersistentMemory()

        if "current_conv_id" not in st.session_state:
            st.session_state.current_conv_id = None

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if "memory_enabled" not in st.session_state:
            st.session_state.memory_enabled = True

        if "agent_thoughts" not in st.session_state:
            st.session_state.agent_thoughts = []

    @staticmethod
    def ensure_conversation(st) -> int:
        """Create a new conversation if none is active; return conv_id."""
        if not st.session_state.current_conv_id:
            conv_id = st.session_state.db.create_conversation()
            st.session_state.current_conv_id = conv_id
        return st.session_state.current_conv_id

    @staticmethod
    def add_chat_message(st, role: str, content: str):
        st.session_state.chat_history.append({"role": role, "content": content})
        if st.session_state.memory_enabled and st.session_state.current_conv_id:
            st.session_state.db.add_message(st.session_state.current_conv_id, role, content)

    @staticmethod
    def add_agent_thought(st, thought_type: str, content: str):
        st.session_state.agent_thoughts.append({"type": thought_type, "content": content})

    @staticmethod
    def clear_agent_thoughts(st):
        st.session_state.agent_thoughts = []

    @staticmethod
    def load_conversation(st, conv_id: int):
        """Switch active conversation and load its messages into chat_history."""
        st.session_state.current_conv_id = conv_id
        messages = st.session_state.db.get_messages(conv_id)
        st.session_state.chat_history = [
            {"role": m["role"], "content": m["content"]} for m in messages
        ]
        st.session_state.agent_thoughts = []

    @staticmethod
    def new_chat(st):
        """Start a fresh conversation."""
        st.session_state.current_conv_id = None
        st.session_state.chat_history = []
        st.session_state.agent_thoughts = []
