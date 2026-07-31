import unittest

from app.agents.intent_classifier import IntentClassifier
from app.agents.router import AgentRouter
from app.core.intents import Intent


class IntentClassifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.classifier = IntentClassifier()

    def assert_intent(self, text: str, expected: Intent) -> None:
        result = self.classifier.classify(text)
        self.assertEqual(expected, result.intent, text)
        self.assertGreaterEqual(result.confidence, 0.5)

    def test_phase_one_intents(self) -> None:
        cases = {
            "วันนี้วันที่เท่าไร": Intent.DATE_QUESTION,
            "ตอนนี้กี่โมง": Intent.TIME_QUESTION,
            "เปิดเพลง Taylor Swift ในยูทูป": Intent.TOOL_ACTION,
            "วันนี้ฉันทำอะไรไปแล้วบ้าง": Intent.MEMORY_QUESTION,
            "สวัสดี เป็นอย่างไรบ้าง": Intent.GENERAL_CHAT,
            "ปิดจาร์วิส": Intent.SYSTEM_COMMAND,
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assert_intent(text, expected)

    def test_future_module_intents_do_not_fall_through(self) -> None:
        self.assert_intent("ไวไฟบ้านมีความเสี่ยงหรือผิดปกติไหม", Intent.NETWORK_RISK)
        self.assert_intent("สรุปเสียงประชุมให้หน่อย", Intent.MEETING_COMMAND)

    def test_today_memory_question_is_not_date(self) -> None:
        self.assert_intent("วันนี้เราคุยอะไรกันไปบ้าง", Intent.MEMORY_QUESTION)


class AgentRouterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.router = AgentRouter()

    def test_date_routes_to_date_tool(self) -> None:
        route = self.router.route("วันนี้วันที่เท่าไร")
        self.assertEqual("get_date", route.tool_name)

    def test_general_chat_has_no_tool(self) -> None:
        route = self.router.route("วันนี้เป็นอย่างไรบ้าง")
        self.assertIsNone(route.tool_name)


if __name__ == "__main__":
    unittest.main()
