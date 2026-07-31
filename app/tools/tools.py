"""
Basic Tools for Jarvis AI

หน้าที่:
- Tool พื้นฐาน เช่น เวลา วันที่ YouTube
- รองรับการเปิด YouTube ธรรมดา
- รองรับการค้นหาเพลง / ค้นหาวิดีโอบน YouTube จากคำพูดผู้ใช้
"""

from __future__ import annotations

import datetime
import re
import webbrowser
from urllib.parse import quote_plus


# ============================
# Time / Date Tools
# ============================

def get_time(_=None):
    """
    Return current time.
    """

    return datetime.datetime.now().strftime("%H:%M:%S")


def get_date(_=None):
    """
    Return current date.
    """

    return datetime.datetime.now().strftime("%Y-%m-%d")


# ============================
# YouTube Tools
# ============================

def extract_youtube_query(user_text: str | None) -> str:
    """
    ดึงชื่อเพลง / คำค้นหา ออกจากประโยคผู้ใช้

    ตัวอย่าง:
    "เปิดเพลง Taylor Swift" -> "Taylor Swift"
    "เปิดยูทูปเพลง Shape of You" -> "Shape of You"
    "หาเพลง night changes ในยูทูป" -> "night changes"
    """

    if not user_text:
        return ""

    text = user_text.strip()

    # ทำให้ช่องว่างไม่มั่ว
    text = re.sub(r"\s+", " ", text)

    # keyword ที่ควรตัดออกจากประโยค
    remove_phrases = [
        # Thai YouTube
        "เปิดยูทูป",
        "เปิดยูทูบ",
        "เปิดยุทูป",
        "เข้ายูทูป",
        "เข้า youtube",
        "เปิด youtube",
        "youtube",
        "ยูทูป",
        "ยูทูบ",
        "yt",

        # Thai music intent
        "เปิดเพลง",
        "เล่นเพลง",
        "หาเพลง",
        "ค้นหาเพลง",
        "เปิดเพลงให้หน่อย",
        "เปิดเพลงให้ที",
        "เปิดเพลงให้ฟังหน่อย",
        "เปิดเพลงในยูทูป",
        "เปิดเพลงบนยูทูป",
        "หาเพลงในยูทูป",
        "ค้นหาเพลงในยูทูป",

        # Video / MV
        "เปิด mv",
        "เปิดเอ็มวี",
        "เปิดมิวสิควีดีโอ",
        "เปิดมิวสิควิดีโอ",

        # English
        "open youtube",
        "play youtube",
        "open yt",
        "play song",
        "play music",
        "open song",
        "search song",
        "search music",
        "search youtube",
        "on youtube",
        "in youtube",

        # polite words
        "ให้หน่อย",
        "ให้ที",
        "หน่อย",
        "ครับ",
        "ค่ะ",
        "คะ",
        "ที",
    ]

    cleaned = text

    # ตัด phrase โดยไม่สนตัวพิมพ์เล็กใหญ่
    for phrase in remove_phrases:
        cleaned = re.sub(
            re.escape(phrase),
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

    # ตัดคำเชื่อมที่มักเหลือ
    cleaned = cleaned.replace("ใน", " ")
    cleaned = cleaned.replace("บน", " ")
    cleaned = cleaned.replace("ให้ฟัง", " ")

    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


def open_youtube(user_text: str | None = None):
    """
    เปิด YouTube

    ถ้าผู้ใช้พูดแค่:
    - เปิดยูทูป
    จะเปิดหน้า YouTube

    ถ้าผู้ใช้พูด:
    - เปิดเพลง Taylor Swift
    - เปิดยูทูปเพลง Shape of You
    จะเปิดหน้า search ของ YouTube ตามคำค้นหา
    """

    query = extract_youtube_query(user_text)

    if query:
        return open_youtube_search(query)

    webbrowser.open("https://www.youtube.com")
    return "Opening YouTube"


def open_youtube_search(query: str | None = None):
    """
    เปิด YouTube search ตาม keyword ที่ได้รับ
    """

    if not query:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"

    search_query = quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={search_query}"

    webbrowser.open(url)

    return f"Opening YouTube search for {query}"


# ============================
# Tool Registry
# ============================

TOOLS = {
    "open_youtube": open_youtube,
    "open_youtube_search": open_youtube_search,
    "get_time": get_time,
    "get_date": get_date,
}