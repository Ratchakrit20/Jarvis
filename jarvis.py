from app.voice.vad import VoiceActivityRecorder
from app.voice.wake_word import WakeWordDetector
from app.voice.stt import WhisperSTT
from app.voice.tts import TTSRouter
from app.agents.jarvis_agent import JarvisAgent


EXIT_WORDS = [
    "ออก",
    "ปิด",
    "หยุด",
    "เลิก",
    "ลาก่อน",
    "exit",
    "quit",
    "stop",
]


def should_exit(text: str) -> bool:
    if not text:
        return False

    text = text.strip().lower()

    # กันเคส "เปิด" โดนเข้าใจผิดว่าเป็น "ปิด"
    non_exit_words = [
        "เปิด",
        "เปิดยูทูป",
        "เปิด youtube",
        "เปิดเพลง",
        "เปิดเว็บ",
        "เปิดโปรแกรม",
    ]

    for word in non_exit_words:
        if word in text:
            return False

    exit_phrases = [
        "ออก",
        "ออกจากระบบ",
        "ปิดจาร์วิส",
        "ปิด jarvis",
        "หยุดทำงาน",
        "เลิกทำงาน",
        "ลาก่อน",
        "exit",
        "quit",
        "stop",
    ]

    return any(phrase == text or phrase in text for phrase in exit_phrases)


def safe_speak(tts: TTSRouter, text: str):
    """
    พูดแบบปลอดภัย

    ถ้า TTS พัง เช่น Edge TTS ต่อเน็ตไม่ได้
    ให้ print error แต่ไม่ทำให้ Jarvis loop หลุด
    """

    if not text:
        return

    try:
        tts.speak(text)

    except Exception as e:
        print("⚠️ TTS Error:", e)
        print("Jarvis ยังทำงานต่อ แต่รอบนี้ไม่ได้พูดออกลำโพง")


def main():
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
            print("\n\n🛑 Jarvis stopped by user")
            break

        except Exception as e:
            print("\n❌ Jarvis Error:", e)
            print("ระบบยังทำงานต่อ สามารถลองสั่งใหม่ได้\n")


if __name__ == "__main__":
    main()