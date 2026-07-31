"""
Basic Tools for Jarvis AI

หน้าที่:
- Tool พื้นฐาน เช่น เวลา วันที่ YouTube
- รองรับการเปิด YouTube ธรรมดา
- รองรับการเล่นผลลัพธ์แรกบน YouTube จากชื่อเพลง
- เปิด Facebook, Instagram และค้นหา Google
"""

from __future__ import annotations

import datetime
import re
import webbrowser
from urllib.parse import quote_plus

from app.core.logger import get_logger


logger = get_logger(__name__)


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


def _find_first_youtube_url(query: str) -> str:
    """Resolve the first YouTube search result without downloading media."""
    try:
        from yt_dlp import YoutubeDL
    except ImportError as exc:
        raise RuntimeError("yt-dlp is not installed") from exc

    options = {
        "extract_flat": True,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }
    with YoutubeDL(options) as downloader:
        result = downloader.extract_info(f"ytsearch1:{query}", download=False)

    entries = result.get("entries") or []
    if not entries:
        raise LookupError(f"No YouTube result found for {query}")

    first = entries[0]
    video_url = first.get("webpage_url") or first.get("url")
    if not video_url:
        raise LookupError(f"YouTube result has no URL for {query}")
    if not str(video_url).startswith("http"):
        video_url = f"https://www.youtube.com/watch?v={video_url}"
    return str(video_url)


def play_youtube_song(user_text: str | None = None):
    """Find the first matching song on YouTube and open it directly."""
    query = extract_youtube_query(user_text)
    if not query:
        return open_youtube(None)

    try:
        url = _find_first_youtube_url(query)
    except Exception as exc:
        logger.warning("Direct YouTube lookup failed query=%s error=%s", query, exc)
        open_youtube_search(query)
        return f"ไม่พบเพลงโดยตรง จึงเปิดหน้าค้นหา YouTube สำหรับ {query}"

    webbrowser.open(url)
    return f"กำลังเล่นเพลง {query}"


# ============================
# Web Tools
# ============================

def open_facebook(_=None):
    """Open Facebook in the default browser."""
    webbrowser.open("https://www.facebook.com/")
    return "กำลังเปิด Facebook"


def open_instagram(_=None):
    """Open Instagram in the default browser."""
    webbrowser.open("https://www.instagram.com/")
    return "กำลังเปิด Instagram"


def extract_google_query(user_text: str | None) -> str:
    """Extract a Google search query from a Thai or English command."""
    if not user_text:
        return ""

    text = re.sub(r"\s+", " ", user_text).strip()
    command_phrases = (
        "ค้นหาในกูเกิล",
        "ค้นหาใน google",
        "ค้นหาบนกูเกิล",
        "ค้นหาบน google",
        "ค้นหากูเกิล",
        "ค้นหา google",
        "หาในกูเกิล",
        "หาใน google",
        "กูเกิล",
        "google search",
        "search google for",
        "search google",
    )
    for phrase in command_phrases:
        text = re.sub(re.escape(phrase), " ", text, flags=re.IGNORECASE)

    for polite_word in ("ให้หน่อย", "หน่อย", "ครับ", "ค่ะ", "คะ"):
        text = text.replace(polite_word, " ")
    return re.sub(r"\s+", " ", text).strip()


def search_google(user_text: str | None = None):
    """Open Google results for a query extracted from the command."""
    query = extract_google_query(user_text)
    if not query:
        webbrowser.open("https://www.google.com")
        return "กำลังเปิด Google"

    url = f"https://www.google.com/search?q={quote_plus(query)}"
    webbrowser.open(url)
    return f"กำลังค้นหา Google เรื่อง {query}"


# ============================
# Tool Registry
# ============================

TOOLS = {
    "open_youtube": open_youtube,
    "open_youtube_search": open_youtube_search,
    "play_youtube_song": play_youtube_song,
    "open_facebook": open_facebook,
    "open_instagram": open_instagram,
    "search_google": search_google,
    "get_time": get_time,
    "get_date": get_date,
}
