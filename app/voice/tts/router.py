import re

from .mms_tts import MMSTTS
from .edge_tts import EdgeTTS
from .processor import clean_text


class TTSRouter:

    def __init__(self):
        self.th = MMSTTS()
        self.en = EdgeTTS()

    def detect_lang(self, text: str):

        if re.search(r"[\u0E00-\u0E7F]", text):
            return "th"

        return "en"

    def speak(self, text: str):

        text = clean_text(text)

        if self.detect_lang(text) == "th":
            self.th.speak(text)
        else:
            self.en.speak(text)