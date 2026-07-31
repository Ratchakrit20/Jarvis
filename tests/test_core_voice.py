import unittest

from app.voice.wake_word import WakeWordDetector
from app.core.commands import should_exit


class ExitCommandTests(unittest.TestCase):
    def test_exit_commands(self) -> None:
        self.assertTrue(should_exit("ปิดจาร์วิส"))
        self.assertTrue(should_exit("exit"))

    def test_open_is_not_exit(self) -> None:
        self.assertFalse(should_exit("เปิดยูทูป"))
        self.assertFalse(should_exit("เปิดเพลง"))


class WakeWordTests(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = WakeWordDetector()

    def test_detects_and_removes_thai_wake_word(self) -> None:
        text = "จาร์วิส วันนี้วันที่เท่าไร"
        self.assertTrue(self.detector.is_wake_word_detected(text))
        self.assertEqual("วันนี้วันที่เท่าไร", self.detector.remove_wake_word(text))

    def test_ignores_command_without_wake_word(self) -> None:
        self.assertFalse(self.detector.is_wake_word_detected("วันนี้วันที่เท่าไร"))


if __name__ == "__main__":
    unittest.main()
