"""
Agent Core Module
Fast-routing + model identity awareness + persistent memory.
"""

import os
import re
from typing import List, Dict, Any, Optional

from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from memory import PersistentMemory


# ── System prompt with model identity injection ───────────────────────────────
SYSTEM_PROMPT = """Current AI Model Information:
- Provider: {provider}
- Model: {model_name}

You are an AI Agent assistant running on the above language model.

If users ask "你是什么模型", "你是谁", "what model are you", "which AI are you" or similar,
answer clearly using the model information above.

You have access to these tools:
{tool_descriptions}

STRICT OUTPUT FORMAT — English keywords only:

When using a tool:
THOUGHT: <reasoning>
ACTION: <Calculator | WebSearch | FileAnalyzer>
ACTION_INPUT: <input for the tool>

When giving the final answer:
THOUGHT: <reasoning>
FINAL_ANSWER: <answer to the user>

RULES:
- Always use ENGLISH keywords: THOUGHT, ACTION, ACTION_INPUT, FINAL_ANSWER
- Never use Chinese keywords like "动作：" or "思考："
- MANDATORY: If user asks to search/find/look up anything or asks about news/current events → MUST use WebSearch. Do NOT answer from memory.
- MANDATORY: If user gives a math expression or asks to calculate → MUST use Calculator.
- MANDATORY: If user asks to read/analyze/summarize a file → MUST use FileAnalyzer.
- Only skip tools for greetings or identity questions.
- Give FINAL_ANSWER only after using the required tool.
- Be concise, helpful, and friendly
"""

# ── Fast-routing patterns (bypass full ReAct for simple tasks) ────────────────
CALC_PATTERN = re.compile(
    r"^[\d\s\+\-\*\/\(\)\.\^%]+$|"
    r"(?:计算|算一下|算出|evaluate|calculate|compute)\s*[:\：]?\s*([\d\s\+\-\*\/\(\)\.\^%]+)",
    re.IGNORECASE
)
FILE_PATTERN = re.compile(
    r"(?:分析|读取|总结|analyze|read|summarize)\s+(.+\.(?:txt|md|markdown))",
    re.IGNORECASE
)

# ── User info extraction patterns ─────────────────────────────────────────────
USER_INFO_PATTERNS = [
    (r"我叫\s*([^\s，。！？,!?]+)", "name"),
    (r"我的名字是\s*([^\s，。！？,!?]+)", "name"),
    (r"我喜欢\s*(.+?)(?:[，。！？]|$)", "likes"),
    (r"我在\s*(.+?)\s*学习", "study_place"),
    (r"我是\s*(.+?)\s*专业", "major"),
    (r"my name is\s+(\w+)", "name"),
    (r"i like\s+(.+?)(?:[,.]|$)", "likes"),
    (r"i study\s+(.+?)(?:[,.]|$)", "study"),
    (r"i'm studying\s+(.+?)(?:[,.]|$)", "study"),
]


class AIAgent:
    """AI Agent with fast routing, model identity, and persistent memory."""

    def __init__(self, tools: List[Tool], db: Optional[PersistentMemory] = None,
                 conv_id: Optional[int] = None):
        self.tools = {tool.name: tool for tool in tools}
        self.tools_list = tools
        self.db = db
        self.conv_id = conv_id
        self.provider = "Unknown"
        self.model_name = "Unknown"
        self.llm = self._initialize_llm()

    def set_conversation(self, conv_id: int):
        self.conv_id = conv_id

    # ── LLM init ──────────────────────────────────────────────────────────────

    def _initialize_llm(self):
        nvidia_key = os.getenv("NVIDIA_API_KEY", "")
        google_key = os.getenv("GOOGLE_API_KEY", "")

        if nvidia_key and nvidia_key != "your_nvidia_api_key_here":
            self.provider = "NVIDIA"
            self.model_name = os.getenv("NVIDIA_MODEL", "meta/llama-3.1-70b-instruct")
            return ChatOpenAI(
                model=self.model_name,
                api_key=nvidia_key,
                base_url=os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"),
                temperature=0.7,
                max_tokens=1024,
            )
        elif google_key and google_key != "your_google_api_key_here":
            self.provider = "Google"
            self.model_name = "gemini-pro"
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=google_key,
                temperature=0.7,
                convert_system_message_to_human=True
            )
        else:
            raise ValueError("No API key found. Set NVIDIA_API_KEY or GOOGLE_API_KEY in .env")

    # ── Prompt ────────────────────────────────────────────────────────────────

    def _build_system_prompt(self) -> str:
        descriptions = "\n".join(f"- {t.name}: {t.description}" for t in self.tools_list)
        return SYSTEM_PROMPT.format(
            provider=self.provider,
            model_name=self.model_name,
            tool_descriptions=descriptions
        )

    # ── Memory context ────────────────────────────────────────────────────────

    def _get_memory_context(self) -> str:
        if not self.db:
            return ""
        parts = []
        user_info = self.db.get_all_user_info()
        if user_info:
            labels = {"name": "Name", "likes": "Likes", "study_place": "Studies at",
                      "major": "Major", "study": "Studies"}
            parts.append("Known user information:")
            for k, v in user_info.items():
                parts.append(f"  - {labels.get(k, k)}: {v}")
        if self.conv_id:
            recent = self.db.get_recent_messages_for_llm(self.conv_id, limit=6)
            if recent:
                parts.append("\nRecent conversation:")
                for msg in recent:
                    role = "User" if msg["role"] == "user" else "Assistant"
                    parts.append(f"  {role}: {msg['content'][:150]}")
        return "\n".join(parts)

    # ── Response parser ───────────────────────────────────────────────────────

    def _parse_response(self, text: str) -> Dict[str, Any]:
        result = {"thought": "", "action": None, "action_input": None, "final_answer": None}
        lines = text.strip().split("\n")
        for i, line in enumerate(lines):
            norm = line.strip().replace("：", ":").replace("**", "")
            upper = norm.upper()
            if re.match(r"^THOUGHT\s*:", upper):
                result["thought"] = re.split(r"THOUGHT\s*:", norm, maxsplit=1, flags=re.IGNORECASE)[-1].strip()
            elif re.match(r"^ACTION_INPUT\s*:", upper):
                result["action_input"] = re.split(r"ACTION_INPUT\s*:", norm, maxsplit=1, flags=re.IGNORECASE)[-1].strip()
            elif re.match(r"^ACTION\s*:", upper):
                result["action"] = re.split(r"ACTION\s*:", norm, maxsplit=1, flags=re.IGNORECASE)[-1].strip()
            elif re.match(r"^FINAL_ANSWER\s*:", upper):
                answer = re.split(r"FINAL_ANSWER\s*:", norm, maxsplit=1, flags=re.IGNORECASE)[-1].strip()
                for j in range(i + 1, len(lines)):
                    answer += "\n" + lines[j]
                result["final_answer"] = answer.strip()
                break
        if result["action"] and result["action_input"] is None:
            result["action_input"] = ""
        return result

    # ── Fast routing ──────────────────────────────────────────────────────────

    def _try_fast_route(self, query: str) -> Optional[Dict[str, Any]]:
        """Bypass full ReAct for simple calculator or file tasks."""
        q = query.strip()

        # Pure math expression
        pure_math = re.match(r"^[\d\s\+\-\*\/\(\)\.\^%]+$", q)
        calc_match = re.search(
            r"(?:计算|算一下|算出|evaluate|calculate|compute)\s*[:\：]?\s*([\d\s\+\-\*\/\(\)\.\^%\*]+)",
            q, re.IGNORECASE
        )
        if pure_math or calc_match:
            expr = q if pure_math else (calc_match.group(1) or q)
            if "Calculator" in self.tools:
                obs = self.tools["Calculator"].func(expr.strip())
                return {
                    "success": True,
                    "output": obs,
                    "steps": [{"thought": "Direct calculation", "action": "Calculator",
                                "action_input": expr.strip(), "observation": obs}]
                }

        # File analysis
        file_match = FILE_PATTERN.search(q)
        if file_match and "FileAnalyzer" in self.tools:
            path = file_match.group(1).strip()
            obs = self.tools["FileAnalyzer"].func(path)
            if not obs.startswith("Error"):
                return {
                    "success": True,
                    "output": obs,
                    "steps": [{"thought": "Direct file read", "action": "FileAnalyzer",
                                "action_input": path, "observation": obs}]
                }

        return None

    # ── Main run ──────────────────────────────────────────────────────────────

    def run(self, query: str) -> Dict[str, Any]:
        # Fast route first
        fast = self._try_fast_route(query)
        if fast:
            return fast

        # Full ReAct loop (max 2 iterations for speed)
        steps = []
        memory_ctx = self._get_memory_context()
        user_content = f"{memory_ctx}\n\nUser query: {query}" if memory_ctx else query
        messages = [
            SystemMessage(content=self._build_system_prompt()),
            HumanMessage(content=user_content)
        ]

        try:
            for _ in range(2):
                response = self.llm.invoke(messages)
                text = response.content
                parsed = self._parse_response(text)

                if parsed["final_answer"]:
                    return {"success": True, "output": parsed["final_answer"], "steps": steps}

                if parsed["action"] and parsed["action_input"] is not None:
                    tool_name = parsed["action"]
                    tool_input = parsed["action_input"]
                    observation = (
                        self.tools[tool_name].func(tool_input)
                        if tool_name in self.tools
                        else f"Tool '{tool_name}' not found. Available: {', '.join(self.tools)}"
                    )
                    steps.append({
                        "thought": parsed["thought"],
                        "action": tool_name,
                        "action_input": tool_input,
                        "observation": str(observation)
                    })
                    messages.append(AIMessage(content=text))
                    messages.append(HumanMessage(
                        content=(
                            f"OBSERVATION: {observation}\n\n"
                            "Now give your FINAL_ANSWER. If file content was returned, summarize it in detail.\n"
                            "THOUGHT: <reasoning>\nFINAL_ANSWER: <answer>"
                        )
                    ))
                else:
                    return {"success": True, "output": text.strip(), "steps": steps}

            return {"success": True, "output": "已完成推理，以上是我找到的信息。", "steps": steps}

        except Exception as e:
            return {"success": False, "output": f"Agent 错误: {str(e)}", "steps": steps}

    # ── User info extraction ──────────────────────────────────────────────────

    def extract_user_info(self, query: str):
        if not self.db:
            return
        for pattern, key in USER_INFO_PATTERNS:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                if value:
                    self.db.save_user_info(key, value)
