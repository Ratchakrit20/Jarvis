import re

from app.core.errors import TTSError
from app.core.logger import get_logger

from .edge_tts import EdgeTTS
from .mms_tts import MMSTTS
from .processor import clean_text


class TTSRouter:
    """Select a TTS engine by language and load it only when first used."""

    def __init__(self):
        self.th = None
        self.en = None
        self.logger = get_logger(self.__class__.__name__)

    def detect_lang(self, text: str):

        if re.search(r"[\u0E00-\u0E7F]", text):
            return "th"

        return "en"

    def speak(self, text: str):
        text = clean_text(text)
        if not text:
            return

        language = self.detect_lang(text)
        try:
            if language == "th":
                if self.th is None:
                    self.th = MMSTTS()
                self.th.speak(text)
                return

            if self.en is None:
                self.en = EdgeTTS()
            self.en.speak(text)
        except Exception as exc:
            self.logger.exception("TTS failed language=%s", language)
            raise TTSError(f"TTS failed for language {language}") from exc
