"""Intent models shared by the Jarvis routing layer."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Intent(str, Enum):
    GENERAL_CHAT = "general_chat"
    MEMORY_QUESTION = "memory_question"
    DATE_QUESTION = "date_question"
    TIME_QUESTION = "time_question"
    TOOL_ACTION = "tool_action"
    SYSTEM_COMMAND = "system_command"
    MEETING_COMMAND = "meeting_command"
    NETWORK_STATUS = "network_status"
    NETWORK_RISK = "network_risk"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class IntentResult:
    """A classified intent with an explainable confidence and reason."""

    intent: Intent
    confidence: float
    reason: str
