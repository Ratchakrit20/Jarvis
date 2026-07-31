"""Route classified user input to a Phase 1 capability."""

from __future__ import annotations

from dataclasses import dataclass

from app.agents.intent_classifier import IntentClassifier
from app.core.intents import Intent, IntentResult
from app.tools.resolver import resolve_tool


@dataclass(frozen=True, slots=True)
class RouteResult:
    """The selected intent and optional registered tool name."""

    classification: IntentResult
    tool_name: str | None = None


class AgentRouter:
    """Select tools only after intent classification has completed."""

    def __init__(self, classifier: IntentClassifier | None = None) -> None:
        self.classifier = classifier or IntentClassifier()

    def route(self, user_text: str) -> RouteResult:
        classification = self.classifier.classify(user_text)
        tool_name = None

        if classification.intent in {
            Intent.DATE_QUESTION,
            Intent.TIME_QUESTION,
            Intent.TOOL_ACTION,
        }:
            tool_name = resolve_tool(None, user_text)

        return RouteResult(classification=classification, tool_name=tool_name)
