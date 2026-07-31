import asyncio
import edge_tts
import os
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

        try:
            await communicate.save(path)
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()

            clock = pygame.time.Clock()
            while pygame.mixer.music.get_busy():
                clock.tick(30)
        finally:
            pygame.mixer.music.unload()
            if os.path.exists(path):
                os.remove(path)

    def speak(self, text: str):
        asyncio.run(self._speak(text))
