from app.voice.microphone import Microphone
from app.voice.stt import WhisperSTT

mic = Microphone()

stt = WhisperSTT()

audio = mic.record()

text = stt.transcribe(audio)

print(text)