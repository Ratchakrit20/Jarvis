def clean_text(text: str):

    text = text.strip()

    # ลดคำแข็ง
    text = text.replace("...", ".")
    text = text.replace("!", ".")
    text = text.replace("?", ".")

    # fix คำ LLM ชอบพูดแล้วเสียงพัง
    text = text.replace("Opening", "กำลังเปิด")
    text = text.replace("YouTube", "ยูทูป")

    return text
