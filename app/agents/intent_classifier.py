"""Deterministic intent classification for Phase 1 voice commands."""

from __future__ import annotations

import re

from app.core.intents import Intent, IntentResult
from app.tools.resolver import normalize_text


class IntentClassifier:
    """Classify common commands before an LLM or tool is selected."""

    _MEMORY_PATTERNS = (
        r"(จำ|เคยคุย|คุย.*อะไร|ทำ.*ไป.*บ้าง|บอก.*ไป)",
        r"(what did (i|we)|remember|previously)",
    )
    _DATE_PATTERNS = (
        r"(วันนี้|พรุ่งนี้|เมื่อวาน).*(วันอะไร|วันที่เท่าไหร่|วันที่เท่าไร)",
        r"^(วันอะไร|วันที่เท่าไหร่|วันที่เท่าไร)$",
        r"\b(what.*date|what day|current date)\b",
    )
    _TIME_PATTERNS = (
        r"(ตอนนี้|ขณะนี้).*(กี่โมง|เวลา)",
        r"^(กี่โมง|เวลาเท่าไหร่|เวลาเท่าไร)$",
        r"\b(what.*time|current time)\b",
    )
    _TOOL_PATTERNS = (
        r"(เปิด|เล่น|ค้นหา|หา|เข้า).*(ยูทู|youtube|เพลง|มิวสิก|mv|facebook|เฟซ|เฟส|instagram|ไอจี|google|กูเกิล)",
        r"\b(open|play|search).*(youtube|song|music|video|facebook|fb|instagram|ig|google)\b",
    )
    _SYSTEM_PATTERNS = (
        r"^(ออก|ปิดจาร์วิส|หยุดทำงาน|เลิกทำงาน|ลาก่อน|exit|quit|stop)$",
    )
    _MEETING_PATTERNS = (
        r"(ประชุม|meeting).*(สรุป|ถอดเสียง|transcript|summary)",
        r"(สรุป|ถอดเสียง).*(ประชุม|meeting)",
    )
    _NETWORK_RISK_PATTERNS = (
        r"(เน็ต|อินเทอร์เน็ต|ไวไฟ|wifi|network).*(เสี่ยง|ผิดปกติ|แปลก|โจมตี|ปลอดภัย)",
        r"(อุปกรณ์|device).*(แปลก|ไม่รู้จัก|เกาะ|เชื่อม).*(ไวไฟ|wifi|network)?",
    )
    _NETWORK_STATUS_PATTERNS = (
        r"(สถานะ|ปริมาณ|การใช้งาน|ช้า).*(เน็ต|อินเทอร์เน็ต|ไวไฟ|wifi|network)",
        r"(เน็ต|อินเทอร์เน็ต|ไวไฟ|wifi|network).*(สถานะ|ใช้งาน|ช้า|อุปกรณ์กี่)",
    )

    @staticmethod
    def _matches(text: str, patterns: tuple[str, ...]) -> bool:
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)

    def classify(self, user_text: str | None) -> IntentResult:
        text = normalize_text(user_text)
        if not text:
            return IntentResult(Intent.UNKNOWN, 1.0, "empty input")

        ordered_rules = (
            (Intent.SYSTEM_COMMAND, self._SYSTEM_PATTERNS, 0.99),
            (Intent.MEMORY_QUESTION, self._MEMORY_PATTERNS, 0.94),
            (Intent.NETWORK_RISK, self._NETWORK_RISK_PATTERNS, 0.94),
            (Intent.NETWORK_STATUS, self._NETWORK_STATUS_PATTERNS, 0.91),
            (Intent.MEETING_COMMAND, self._MEETING_PATTERNS, 0.92),
            (Intent.TIME_QUESTION, self._TIME_PATTERNS, 0.97),
            (Intent.DATE_QUESTION, self._DATE_PATTERNS, 0.97),
            (Intent.TOOL_ACTION, self._TOOL_PATTERNS, 0.95),
        )
        for intent, patterns, confidence in ordered_rules:
            if self._matches(text, patterns):
                return IntentResult(intent, confidence, f"matched {intent.value} rule")

        return IntentResult(Intent.GENERAL_CHAT, 0.60, "no specialized rule matched")
