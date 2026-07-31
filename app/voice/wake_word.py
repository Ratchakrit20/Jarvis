"""
Wake Word Detection

Author : JarvisAI

หน้าที่:
- ตรวจว่าข้อความจาก STT มีคำปลุก Jarvis หรือไม่
- รองรับไทย/อังกฤษ
- รองรับคำที่ Whisper ถอดเสียงเพี้ยน
- รองรับ fuzzy matching แบบเบา ๆ
"""

from __future__ import annotations

from difflib import SequenceMatcher

from app.config import WAKE_WORD


class WakeWordDetector:
    def __init__(self):
        self.wake_words = [
            WAKE_WORD,

            # English
            "jarvis",
            "jar ves",
            "jar viss",
            "jarvice",
            "javis",

            # Thai normal
            "จาร์วิส",
            "จาวิส",
            "จาวิด",
            "จาร์วิด",
            "จาวิสต์",
            "จาร์วิสท์",
            "เจวิส",
            "เจอร์วิส",

            # Whisper mistakes from real test
            "ดาวิส",
            "จาวิช",
            "ดาวิช",
            "ดาร์วิส",
            "ชาวิส",
            "ชาวิช",
        ]

        # ยิ่งสูงยิ่ง strict
        # 0.72 คือยอมให้เพี้ยนได้พอสมควร
        self.fuzzy_threshold = 0.72

    def normalize(self, text: str) -> str:
        if not text:
            return ""

        text = text.strip().lower()

        replacements = {
            ".": "",
            ",": "",
            "?": "",
            "!": "",
            "ๆ": "",
            "ครับ": "",
            "ค่ะ": "",
            "คะ": "",
            "ฮะ": "",
            "นะ": "",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text.strip()

    def normalize_no_space(self, text: str) -> str:
        return self.normalize(text).replace(" ", "")

    def similarity(self, a: str, b: str) -> float:
        if not a or not b:
            return 0.0

        return SequenceMatcher(None, a, b).ratio()

    def is_wake_word_detected(self, text: str) -> bool:
        if not text:
            return False

        normalized_text = self.normalize(text)
        normalized_no_space = self.normalize_no_space(text)

        if not normalized_text:
            return False

        # 1. Direct contains แบบไม่สนช่องว่าง
        for word in self.wake_words:
            normalized_word = self.normalize_no_space(word)

            if normalized_word and normalized_word in normalized_no_space:
                return True

        # 2. Token fuzzy matching
        # เช่น "จาวิช วันนี้วันอะไร" ให้ token "จาวิช" เทียบกับ "จาวิส"
        tokens = normalized_text.split()

        for token in tokens:
            clean_token = self.normalize_no_space(token)

            for word in self.wake_words:
                clean_word = self.normalize_no_space(word)

                if not clean_token or not clean_word:
                    continue

                score = self.similarity(clean_token, clean_word)

                if score >= self.fuzzy_threshold:
                    return True

        return False

    def remove_wake_word(self, text: str) -> str:
        """
        ตัด wake word ออกจากข้อความ เพื่อส่งคำสั่งจริงเข้า Agent

        ตัวอย่าง:
        "จาร์วิส วันนี้วันอะไร" -> "วันนี้วันอะไร"
        "จาวิช วันนี้วันอะไร" -> "วันนี้วันอะไร"
        """

        if not text:
            return ""

        original_tokens = text.strip().split()
        cleaned_tokens = []

        for token in original_tokens:
            token_normalized = self.normalize_no_space(token)

            is_wake_token = False

            for word in self.wake_words:
                word_normalized = self.normalize_no_space(word)

                if not word_normalized:
                    continue

                # direct
                if token_normalized == word_normalized:
                    is_wake_token = True
                    break

                # fuzzy
                score = self.similarity(token_normalized, word_normalized)
                if score >= self.fuzzy_threshold:
                    is_wake_token = True
                    break

            if not is_wake_token:
                cleaned_tokens.append(token)

        return " ".join(cleaned_tokens).strip()