import asyncio
import edge_tts
import tempfile
import pygame


class EdgeTTS:

    def __init__(self):
        pygame.mixer.init()

    async def _speak(self, text: str):

        communicate = edge_tts.Communicate(
            text,
            "en-US-JennyNeural"
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            path = f.name

        await communicate.save(path)

        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            continue

    def speak(self, text: str):
        asyncio.run(self._speak(text))