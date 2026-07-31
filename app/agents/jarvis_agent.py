# app/agent/jarvis_agent.py
import json
from app.llm.ollama import OllamaLLM
from app.tools.resolver import resolve_tool
from memory.memory import Memory
from app.tools.tools import TOOLS


SYSTEM_PROMPT = """
You are Jarvis.

You MUST ALWAYS output JSON only.

NO EXCEPTIONS.

If user input matches a tool, you MUST use tool.

TOOLS:

- open_youtube → open YouTube
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
    def __init__(self):
        self.llm = OllamaLLM()
        self.memory = Memory()
    def _safe_parse(self, raw: str):
        try:
            return json.loads(raw)
        except:
            return None
    def chat(self, text: str):

        self.memory.add_user(text)

        # 🔥 STEP 1: try resolver FIRST
        tool = resolve_tool(None, text)

        if tool:
            if tool in TOOLS:
                result = TOOLS[tool](text)
                self.memory.add_assistant(result)
                return result

        # 🔥 STEP 2: LLM fallback
        res = self.llm.client.chat(
            model=self.llm.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *self.memory.get(10),
                {"role": "user", "content": text},
            ],
            options={"temperature": 0.2},
        )

        raw = res["message"]["content"].strip()

        data = self._safe_parse(raw)

        if not data:
            return raw

        answer = data.get("answer", "")

        self.memory.add_assistant(answer)

        return answer