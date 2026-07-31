from app.agents.jarvis_agent import JarvisAgent
from app.core.commands import should_exit
from app.core.logger import get_logger
from app.voice.stt import WhisperSTT
from app.voice.tts import TTSRouter
from app.voice.vad import VoiceActivityRecorder
from app.voice.wake_word import WakeWordDetector


logger = get_logger("jarvis")


def safe_speak(tts: TTSRouter, text: str) -> bool:
    """
    พูดแบบปลอดภัย

    ถ้า TTS พัง เช่น Edge TTS ต่อเน็ตไม่ได้
    ให้ print error แต่ไม่ทำให้ Jarvis loop หลุด
    """

    if not text:
        return False

    try:
        tts.speak(text)
        return True

    except Exception as e:
        logger.exception("TTS playback failed")
        print("⚠️ TTS Error:", e)
        print("Jarvis ยังทำงานต่อ แต่รอบนี้ไม่ได้พูดออกลำโพง")
        return False


def main():
    logger.info("Jarvis starting")
    print("\n====== Initializing Jarvis ======\n")

    vad = VoiceActivityRecorder()
    wake_word = WakeWordDetector()
    stt = WhisperSTT()
    tts = TTSRouter()
    agent = JarvisAgent()

    print("\n====== Jarvis Ready ======")
    print("โหมด: Wake Word + VAD")
    print('พูดว่า "จาร์วิส" หรือ "Jarvis" ก่อนสั่งงาน')
    print("ตัวอย่าง: จาร์วิส วันนี้วันอะไร")
    print("กด Ctrl + C เพื่อปิดระบบ")
    print("==========================\n")

    while True:
        try:
            audio = vad.listen()

            if audio is None:
                continue

            text = stt.transcribe(audio)
            logger.info("speech_transcribed has_text=%s", bool(text))

            print()
            print("HEARD :", text)

            if not text:
                print("⚠️ Whisper ไม่ได้ข้อความ ลองพูดใหม่อีกครั้ง")
                continue

            # อนุญาตให้ออกได้แม้ไม่เรียก Wake Word
            if should_exit(text):
                goodbye = "ลาก่อนครับ"
                print("Jarvis :", goodbye)
                safe_speak(tts, goodbye)
                break

            if not wake_word.is_wake_word_detected(text):
                print('💤 ยังไม่ได้ยิน Wake Word ข้ามคำสั่งนี้')
                print('ต้องพูดว่า "จาร์วิส" หรือ "Jarvis" ก่อน')
                continue

            command = wake_word.remove_wake_word(text)
            logger.info("wake_word_detected command_length=%d", len(command))

            print("COMMAND :", command)

            if not command:
                ready_text = "ครับ ผมฟังอยู่"
                print("Jarvis :", ready_text)
                safe_speak(tts, ready_text)
                continue

            reply = agent.chat(command)

            print()
            print("Jarvis :", reply)

            safe_speak(tts, reply)

        except KeyboardInterrupt:
            logger.info("Jarvis stopped by user")
            print("\n\n🛑 Jarvis stopped by user")
            break

        except Exception as e:
            logger.exception("Unhandled main-loop error")
            print("\n❌ Jarvis Error:", e)
            print("ระบบยังทำงานต่อ สามารถลองสั่งใหม่ได้\n")


if __name__ == "__main__":
    main()
