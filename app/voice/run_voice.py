from app.voice.recorder import record_audio
from app.voice.stt import WhisperSTT
from app.voice.tts import TTSRouter
from app.agents.jarvis_agent import JarvisAgent



# init all engines
stt = WhisperSTT()
tts = TTSRouter()
agent = JarvisAgent()


print("\n🚀 Jarvis Voice Ready\n")

while True:

    input("🎤 กด Enter เพื่อพูด...")

    # 1. record
    audio = record_audio(seconds=5)

    # 2. STT
    text = stt.transcribe(audio)
    print("👤:", text)

    if not text:
        continue

    # 3. Agent
    reply = agent.chat(text)
    print("🤖:", reply)

    # 4. TTS
    tts.speak(reply)