# app/agent/jarvis_agent.py
import json

from app.agents.router import AgentRouter
from app.core.intents import Intent
from app.core.logger import get_logger
from app.llm.ollama import OllamaLLM
from memory.memory import Memory
from app.tools.tools import TOOLS


SYSTEM_PROMPT = """
You are Jarvis.

You MUST ALWAYS output JSON only.

NO EXCEPTIONS.

If user input matches a tool, you MUST use tool.

TOOLS:

- open_youtube → open YouTube
- play_youtube_song → play the first matching YouTube song
- open_facebook → open Facebook
- open_instagram → open Instagram
- search_google → search Google
- get_time → get current time
- get_date → get current date

RULE:

If tool is needed:
{
  "tool": "tool_name",
  "input": ""
}

If no tool:
{
  "tool": null,
  "answer": "response"
}

IMPORTANT:
- Output ONLY JSON
- No text before or after
- No explanation
"""


class JarvisAgent:
    """Route a command to a deterministic tool or the conversational LLM."""

    def __init__(self, llm=None, memory=None, router=None):
        self.llm = llm or OllamaLLM()
        self.memory = memory or Memory()
        self.router = router or AgentRouter()
        self.logger = get_logger(self.__class__.__name__)

    def _safe_parse(self, raw: str):
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return None

    def _chat_with_llm(self, text: str) -> str:
        history = self.memory.get(10)
        response = self.llm.client.chat(
            model=self.llm.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *history,
                {"role": "user", "content": text},
            ],
            options={"temperature": 0.2},
        )
        raw = response["message"]["content"].strip()
        data = self._safe_parse(raw)
        if not data:
            return raw
        return str(data.get("answer") or raw)

    def chat(self, text: str) -> str:
        if not text or not text.strip():
            return "ผมยังไม่ได้ยินคำสั่งครับ"

        route = self.router.route(text)
        intent = route.classification.intent
        self.logger.info(
            "intent=%s confidence=%.2f tool=%s",
            intent.value,
            route.classification.confidence,
            route.tool_name,
        )

        if intent in {Intent.NETWORK_RISK, Intent.NETWORK_STATUS}:
            return "โมดูลตรวจสอบเครือข่ายยังไม่เปิดใช้งานครับ"
        if intent is Intent.MEETING_COMMAND:
            return "โมดูลสรุปการประชุมยังไม่เปิดใช้งานครับ"
        if intent is Intent.SYSTEM_COMMAND:
            return "ลาก่อนครับ"

        if route.tool_name in TOOLS:
            answer = str(TOOLS[route.tool_name](text))
            self.memory.add_user(text)
            self.memory.add_assistant(answer)
            return answer

        try:
            answer = self._chat_with_llm(text)
        except Exception as exc:
            self.logger.exception("LLM request failed")
            return f"ขออภัยครับ ระบบภาษาใช้งานไม่ได้ชั่วคราว: {exc}"

        self.memory.add_user(text)
        self.memory.add_assistant(answer)
        return answer
