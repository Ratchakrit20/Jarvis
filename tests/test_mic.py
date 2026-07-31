from app.voice.microphone import Microphone

mic = Microphone()

audio = mic.record()

print(audio.shape)