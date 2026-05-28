"""
AI Agent Assistant — Modern UI v2
ChatGPT/Claude style, persistent SQLite memory, fast-routed agent.
"""

import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from memory import PersistentMemory, SessionMemory
from tools.search_tool import create_search_tool
from tools.calculator_tool import create_calculator_tool
from tools.file_tool import create_file_tool

load_dotenv()

st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #f7f7f8;
    border-right: 1px solid #e5e5e5;
    min-width: 240px !important;
    max-width: 260px !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 1rem 0.75rem;
}

/* New Chat button */
div[data-testid="stButton"].new-chat > button {
    background: #2563eb !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: background 0.15s;
}
div[data-testid="stButton"].new-chat > button:hover {
    background: #1d4ed8 !important;
}

/* Conversation group label */
.conv-group {
    font-size: 0.68rem;
    font-weight: 700;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.6rem 0 0.2rem;
}

/* Tool cards */
.tool-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 0.45rem 0.7rem;
    margin: 0.2rem 0;
    font-size: 0.82rem;
    color: #374151;
    transition: border-color 0.15s;
}
.tool-card:hover { border-color: #93c5fd; }

/* Memory box */
.memory-box {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 0.55rem 0.7rem;
    font-size: 0.8rem;
    color: #374151;
    line-height: 1.65;
}

/* ── Main area ── */
.main .block-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0.5rem 1.5rem 5rem;
}

/* Top bar */
.topbar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 0 0.75rem;
    border-bottom: 1px solid #e5e7eb;
    margin-bottom: 1.25rem;
}
.topbar-title {
    font-size: 1rem;
    font-weight: 700;
    color: #111827;
    flex: 1;
}
.badge {
    font-size: 0.68rem;
    font-weight: 600;
    padding: 0.2rem 0.55rem;
    border-radius: 20px;
    letter-spacing: 0.02em;
}
.badge-provider {
    background: #dbeafe;
    color: #1d4ed8;
}
.badge-model {
    background: #f3f4f6;
    color: #6b7280;
    max-width: 160px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* ── Chat bubbles ── */
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.75rem 0;
}
.msg-user .bubble {
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    color: white;
    padding: 0.7rem 1.1rem;
    border-radius: 20px 20px 5px 20px;
    max-width: 72%;
    font-size: 0.9rem;
    line-height: 1.55;
    white-space: pre-wrap;
    box-shadow: 0 1px 3px rgba(37,99,235,0.25);
}
.msg-assistant {
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
    margin: 0.75rem 0;
}
.msg-avatar {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem;
    flex-shrink: 0;
    margin-top: 3px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.12);
}
.msg-assistant .bubble {
    background: white;
    border: 1px solid #e5e7eb;
    color: #111827;
    padding: 0.7rem 1.1rem;
    border-radius: 5px 20px 20px 20px;
    max-width: 78%;
    font-size: 0.9rem;
    line-height: 1.65;
    white-space: pre-wrap;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

/* ── Reasoning timeline ── */
.reasoning-wrap {
    margin: 0.3rem 0;
    border-left: 2px solid #e5e7eb;
    padding-left: 0.75rem;
}
.reasoning-step {
    display: flex;
    gap: 0.6rem;
    margin: 0.35rem 0;
    align-items: flex-start;
}
.r-dot {
    width: 9px; height: 9px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
}
.dot-t { background: #3b82f6; }
.dot-a { background: #10b981; }
.dot-o { background: #f59e0b; }
.r-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 0.4rem 0.65rem;
    flex: 1;
    font-size: 0.81rem;
    color: #4b5563;
    line-height: 1.5;
}
.r-label {
    font-weight: 700;
    font-size: 0.72rem;
    margin-bottom: 2px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.lbl-t { color: #2563eb; }
.lbl-a { color: #059669; }
.lbl-o { color: #d97706; }

/* Welcome screen */
.welcome {
    text-align: center;
    padding: 3rem 1rem;
    color: #9ca3af;
}
.welcome h2 { font-size: 1.4rem; color: #374151; margin-bottom: 0.5rem; }
.welcome p  { font-size: 0.9rem; }
.welcome-chips {
    display: flex; flex-wrap: wrap; gap: 0.5rem;
    justify-content: center; margin-top: 1.5rem;
}
.chip {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 0.4rem 0.9rem;
    font-size: 0.82rem;
    color: #374151;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)


# ── Cached agent init ─────────────────────────────────────────────────────────

@st.cache_resource
def get_agent(_db: PersistentMemory):
    from agent_core import AIAgent
    tools = [create_search_tool(), create_calculator_tool(), create_file_tool()]
    return AIAgent(tools=tools, db=_db)


# ── App init ──────────────────────────────────────────────────────────────────

def initialize_app():
    SessionMemory.initialize_session_state(st)

    if "agent" not in st.session_state:
        st.session_state.agent = get_agent(st.session_state.db)

    if "uploaded_file_path" not in st.session_state:
        st.session_state.uploaded_file_path = None


# ── Sidebar ───────────────────────────────────────────────────────────────────

def render_sidebar():
    db: PersistentMemory = st.session_state.db

    with st.sidebar:
        if st.button("✏️  New Chat", use_container_width=True, key="new_chat_btn"):
            SessionMemory.new_chat(st)
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # History
        groups = db.group_conversations_by_date()
        if any(groups.values()):
            for label, convs in groups.items():
                if not convs:
                    continue
                st.markdown(f'<div class="conv-group">{label}</div>', unsafe_allow_html=True)
                for c in convs:
                    is_active = st.session_state.current_conv_id == c["id"]
                    btn_type = "primary" if is_active else "secondary"
                    if st.button(
                        c["title"], key=f"conv_{c['id']}",
                        use_container_width=True, type=btn_type
                    ):
                        SessionMemory.load_conversation(st, c["id"])
                        st.session_state.agent.set_conversation(c["id"])
                        st.rerun()
        else:
            st.caption("暂无历史对话")

        st.markdown("---")

        # Tools
        st.markdown("**🛠 Tools**")
        for icon, name, desc in [
            ("🔍", "Web Search", "搜索互联网"),
            ("🧮", "Calculator", "数学计算"),
            ("📄", "File Analyzer", "分析文本文件"),
        ]:
            st.markdown(
                f'<div class="tool-card">{icon} <strong>{name}</strong>'
                f'<br><span style="color:#9ca3af;font-size:0.75rem">{desc}</span></div>',
                unsafe_allow_html=True
            )

        st.markdown("---")

        # File upload
        st.markdown("**📂 Upload File**")
        uploaded = st.file_uploader(
            "拖拽 .txt / .md", type=["txt", "md"], label_visibility="collapsed"
        )
        if uploaded:
            suffix = os.path.splitext(uploaded.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode="wb") as tmp:
                tmp.write(uploaded.getvalue())
                st.session_state.uploaded_file_path = tmp.name
            st.success(f"✅ {uploaded.name}")
            if st.button("🔍 分析文件", use_container_width=True):
                process_user_input(f"请分析这个文件：{st.session_state.uploaded_file_path}")
                st.rerun()

        st.markdown("---")

        # Memory
        st.markdown("**💾 Memory**")
        summary = db.get_context_summary()
        st.markdown(f'<div class="memory-box">{summary}</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.session_state.memory_enabled = st.toggle(
                "开启", value=st.session_state.memory_enabled, key="mem_toggle"
            )
        with c2:
            if st.button("清空", use_container_width=True, key="clear_mem"):
                db.clear_user_info()
                st.rerun()


# ── Chat rendering ────────────────────────────────────────────────────────────

def render_chat():
    if not st.session_state.chat_history:
        agent = st.session_state.agent
        st.markdown(f"""
        <div class="welcome">
            <h2>👋 你好，我是 AI Agent</h2>
            <p>运行于 <strong>{agent.provider}</strong> · <strong>{agent.model_name.split("/")[-1]}</strong></p>
            <p style="margin-top:0.5rem;color:#6b7280">我可以搜索网页、进行计算、分析文件，并记住我们的对话。</p>
            <div class="welcome-chips">
                <span class="chip">🔍 搜索最新 AI 新闻</span>
                <span class="chip">🧮 计算 18*25+99</span>
                <span class="chip">📄 分析 README.md</span>
                <span class="chip">💬 你是什么模型？</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            content = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
            st.markdown(
                f'<div class="msg-user"><div class="bubble">{content}</div></div>',
                unsafe_allow_html=True
            )
        else:
            content = msg["content"].replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
            st.markdown(
                f'<div class="msg-assistant">'
                f'<div class="msg-avatar">🤖</div>'
                f'<div class="bubble">{content}</div>'
                f'</div>',
                unsafe_allow_html=True
            )


def render_reasoning():
    if not st.session_state.agent_thoughts:
        return
    with st.expander("🧠 Agent 推理过程", expanded=False):
        st.markdown('<div class="reasoning-wrap">', unsafe_allow_html=True)
        for step in st.session_state.agent_thoughts:
            t = step["type"]
            c = step["content"].replace("<", "&lt;").replace(">", "&gt;")
            if t == "thought":
                dot, lbl_cls, label = "dot-t", "lbl-t", "💭 THOUGHT"
            elif t == "action":
                dot, lbl_cls, label = "dot-a", "lbl-a", "⚡ ACTION"
            else:
                # Truncate long observations
                if len(c) > 300:
                    c = c[:300] + "…"
                dot, lbl_cls, label = "dot-o", "lbl-o", "👁 OBSERVATION"
            st.markdown(
                f'<div class="reasoning-step">'
                f'<div class="r-dot {dot}"></div>'
                f'<div class="r-card">'
                f'<div class="r-label {lbl_cls}">{label}</div>{c}'
                f'</div></div>',
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)


# ── Core logic ────────────────────────────────────────────────────────────────

def process_user_input(user_input: str):
    SessionMemory.clear_agent_thoughts(st)

    conv_id = SessionMemory.ensure_conversation(st)
    st.session_state.agent.set_conversation(conv_id)

    # Auto-title on first message
    db: PersistentMemory = st.session_state.db
    conv = db.get_conversation(conv_id)
    if conv and conv["title"] == "New Chat":
        db.update_title(conv_id, user_input[:30].strip())

    SessionMemory.add_chat_message(st, "user", user_input)

    with st.spinner("思考中…"):
        result = st.session_state.agent.run(user_input)

    for step in result.get("steps", []):
        SessionMemory.add_agent_thought(st, "thought", step.get("thought") or "分析查询…")
        SessionMemory.add_agent_thought(
            st, "action",
            f"工具: {step['action']}  |  输入: {step['action_input']}"
        )
        SessionMemory.add_agent_thought(st, "observation", step["observation"][:400])

    SessionMemory.add_chat_message(st, "assistant", result["output"])

    if st.session_state.memory_enabled:
        st.session_state.agent.extract_user_info(user_input)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    initialize_app()
    render_sidebar()

    agent = st.session_state.agent
    provider = agent.provider
    model_short = agent.model_name.split("/")[-1]

    st.markdown(
        f'<div class="topbar">'
        f'<span class="topbar-title">🤖 AI Agent Assistant</span>'
        f'<span class="badge badge-provider">{provider}</span>'
        f'<span class="badge badge-model">{model_short}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    render_chat()
    render_reasoning()

    user_input = st.chat_input("发消息… 可搜索、计算、分析文件")
    if user_input:
        process_user_input(user_input)
        st.rerun()


if __name__ == "__main__":
    nvidia_key = os.getenv("NVIDIA_API_KEY", "")
    google_key = os.getenv("GOOGLE_API_KEY", "")
    if not nvidia_key.strip() and not google_key.strip():
        st.error("⚠️ 未找到 API Key，请在 .env 中配置 NVIDIA_API_KEY 或 GOOGLE_API_KEY")
        st.stop()
    main()
