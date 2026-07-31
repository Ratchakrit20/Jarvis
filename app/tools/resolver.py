"""
Tool Resolver

หน้าที่:
- รับ tool_name จาก LLM ถ้ามี
- ถ้า LLM ไม่ได้ส่ง tool มา ให้เดาจากข้อความผู้ใช้
- รองรับภาษาไทย / อังกฤษ / คำพูดธรรมชาติ / คำสะกดผิดบางส่วน
- รองรับ YouTube Search / เปิดเพลงตามชื่อ
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher


# ============================
# Tool Aliases
# ============================

TOOL_ALIASES = {
    "open_youtube": [
        # English
        "youtube",
        "open youtube",
        "open yt",
        "yt",
        "play youtube",
        "watch youtube",

        # Thai normal
        "เปิดยูทูป",
        "เปิด youtube",
        "เข้า youtube",
        "เข้ายูทูป",
        "ยูทูป",
        "ดูยูทูป",
        "เล่นยูทูป",

        # Common STT / typo
        "เปดยทป",
        "เปิดยุทูป",
        "เปิดยูทุป",
        "เปิดยูทูบ",
        "ยูทูบ",
        "ยูทุป",
        "ยุทูป",
    ],

    "open_youtube_search": [
        # Thai music
        "เปิดเพลง",
        "เล่นเพลง",
        "หาเพลง",
        "ค้นหาเพลง",
        "เปิดเพลงในยูทูป",
        "เปิดเพลงบนยูทูป",
        "หาเพลงในยูทูป",
        "ค้นหาเพลงในยูทูป",
        "เปิดเพลงให้ฟัง",
        "เปิดเพลงให้หน่อย",
        "เปิดเพลงให้ที",

        # MV / video
        "เปิด mv",
        "เปิดเอ็มวี",
        "เปิดมิวสิควีดีโอ",
        "เปิดมิวสิควิดีโอ",

        # English
        "play song",
        "play music",
        "open song",
        "search song",
        "search music",
        "search youtube",
        "youtube search",
    ],

    "get_time": [
        # English
        "time",
        "what time",
        "what time is it",
        "current time",
        "tell me the time",
        "now time",

        # Thai
        "เวลา",
        "กี่โมง",
        "ตอนนี้กี่โมง",
        "ตอนนี้เวลาอะไร",
        "ตอนนี้เวลาเท่าไหร่",
        "ตอนนี้เวลาเท่าไร",
        "บอกเวลา",
        "ขอเวลา",
        "เวลากี่โมง",
        "กี่โมงแล้ว",
        "เวลาตอนนี้",
    ],

    "get_date": [
        # English
        "date",
        "what date",
        "what is the date",
        "today date",
        "current date",

        # Thai direct date questions
        "วันที่",
        "วันนี้วันที่เท่าไหร่",
        "วันนี้วันที่เท่าไร",
        "วันนี้วันอะไร",
        "วันนี้วันไหน",
        "วันนี้วันที่อะไร",
        "บอกวันที่",
        "ขอวันที่",
        "วันอะไร",
        "วันไหน",
        "วันที่เท่าไหร่",
        "วันที่เท่าไร",
    ],
}


# ============================
# Patterns
# ============================

YOUTUBE_SEARCH_PATTERNS = [
    r"เปิด\s*เพลง",
    r"เล่น\s*เพลง",
    r"หา\s*เพลง",
    r"ค้นหา\s*เพลง",
    r"เปิด\s*เพลง.*ยู\s*ทูป",
    r"เปิด\s*เพลง.*youtube",
    r"หา\s*เพลง.*ยู\s*ทูป",
    r"หา\s*เพลง.*youtube",
    r"เปิด\s*mv",
    r"เปิด\s*เอ็มวี",
    r"เปิด\s*มิวสิค",
    r"play\s+song",
    r"play\s+music",
    r"search\s+song",
    r"search\s+music",
]

YOUTUBE_PATTERNS = [
    r"เปิด\s*ยู\s*ทูป",
    r"เปิด\s*youtube",
    r"เข้า\s*ยู\s*ทูป",
    r"เข้า\s*youtube",
    r"ดู\s*ยู\s*ทูป",
    r"เล่น\s*ยู\s*ทูป",
    r"open\s+youtube",
    r"watch\s+youtube",
]

DATE_PATTERNS = [
    r"วันนี้\s*วัน\s*อะไร",
    r"วันนี้\s*วัน\s*ไหน",
    r"วันนี้\s*วันที่\s*(เท่าไหร่|เท่าไร|อะไร)",
    r"วันที่\s*(เท่าไหร่|เท่าไร|อะไร)",
    r"ตอนนี้\s*วันที่\s*(เท่าไหร่|เท่าไร|อะไร)",
    r"ขอ\s*วันที่",
    r"บอก\s*วันที่",
]

TIME_PATTERNS = [
    r"ตอนนี้\s*กี่โมง",
    r"กี่โมง\s*แล้ว",
    r"เวลา\s*(อะไร|เท่าไหร่|เท่าไร)",
    r"ตอนนี้\s*เวลา\s*(อะไร|เท่าไหร่|เท่าไร)",
    r"ขอ\s*เวลา",
    r"บอก\s*เวลา",
]


# ข้อความพวกนี้มีคำว่า "วันนี้" แต่ไม่ควรเรียก Date Tool
MEMORY_OR_GENERAL_TODAY_PATTERNS = [
    r"วันนี้.*ทำ.*อะไร",
    r"ทำ.*อะไร.*วันนี้",
    r"วันนี้.*ทำ.*ไป.*บ้าง",
    r"ทำ.*ไป.*บ้าง.*วันนี้",
    r"วันนี้.*คุย.*อะไร",
    r"คุย.*อะไร.*วันนี้",
    r"วันนี้.*จำ.*อะไร",
    r"วันนี้.*มีอะไร.*บ้าง",
]


# ============================
# Helpers
# ============================

def normalize_text(text: str | None) -> str:
    if not text:
        return ""

    text = text.lower().strip()

    replacements = {
        "ๆ": "",
        "ฯ": "",
        ".": "",
        ",": "",
        "?": "",
        "!": "",
        "ครับ": "",
        "ค่ะ": "",
        "คะ": "",
        "ฮะ": "",
        "หน่อย": "",
        "ให้หน่อย": "",
        "ให้ที": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_no_space(text: str | None) -> str:
    return normalize_text(text).replace(" ", "")


def similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0

    return SequenceMatcher(None, a, b).ratio()


def match_patterns(text: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if re.search(pattern, text):
            return True

    return False


def match_alias(text: str, aliases: list[str]) -> bool:
    normalized_text = normalize_text(text)
    no_space_text = normalize_no_space(text)

    for alias in aliases:
        normalized_alias = normalize_text(alias)
        no_space_alias = normalize_no_space(alias)

        if not normalized_alias:
            continue

        if normalized_alias in normalized_text:
            return True

        if no_space_alias in no_space_text:
            return True

    return False


def fuzzy_match_alias(text: str, aliases: list[str], threshold: float = 0.84) -> bool:
    normalized_text = normalize_text(text)
    tokens = normalized_text.split()

    for token in tokens:
        clean_token = normalize_no_space(token)

        for alias in aliases:
            clean_alias = normalize_no_space(alias)

            if not clean_token or not clean_alias:
                continue

            if len(clean_alias) > 12:
                continue

            score = similarity(clean_token, clean_alias)

            if score >= threshold:
                return True

    return False


def is_memory_or_general_today_question(text: str) -> bool:
    normalized_text = normalize_text(text)

    return match_patterns(normalized_text, MEMORY_OR_GENERAL_TODAY_PATTERNS)


# ============================
# Main Resolver
# ============================

def resolve_tool(tool_name: str | None, user_text: str):
    """
    Resolve tool from LLM tool_name or user text.

    Return:
        tool name เช่น
        - open_youtube
        - open_youtube_search
        - get_time
        - get_date
        หรือ None ถ้าไม่ควรใช้ tool
    """

    # 1) ถ้า LLM ส่ง tool มาแล้ว ใช้ก่อน
    if tool_name:
        return tool_name

    text = normalize_text(user_text)

    if not text:
        return None

    # 2) กันกรณีคำถามทั่วไปเกี่ยวกับวันนี้
    # เช่น "นายทำอะไรไปแล้วบ้างวันนี้"
    if is_memory_or_general_today_question(text):
        return None

    # 3) YouTube Search / เปิดเพลง ต้องมาก่อน open_youtube ธรรมดา
    if match_patterns(text, YOUTUBE_SEARCH_PATTERNS):
        return "open_youtube_search"

    if match_alias(text, TOOL_ALIASES["open_youtube_search"]):
        return "open_youtube_search"

    if fuzzy_match_alias(text, TOOL_ALIASES["open_youtube_search"], threshold=0.82):
        return "open_youtube_search"

    # 4) YouTube ธรรมดา
    if match_patterns(text, YOUTUBE_PATTERNS):
        return "open_youtube"

    if match_alias(text, TOOL_ALIASES["open_youtube"]):
        return "open_youtube"

    if fuzzy_match_alias(text, TOOL_ALIASES["open_youtube"], threshold=0.82):
        return "open_youtube"

    # 5) Time
    if match_patterns(text, TIME_PATTERNS):
        return "get_time"

    if match_alias(text, TOOL_ALIASES["get_time"]):
        return "get_time"

    if fuzzy_match_alias(text, TOOL_ALIASES["get_time"], threshold=0.86):
        return "get_time"

    # 6) Date
    if match_patterns(text, DATE_PATTERNS):
        return "get_date"

    if match_alias(text, TOOL_ALIASES["get_date"]):
        return "get_date"

    if fuzzy_match_alias(text, TOOL_ALIASES["get_date"], threshold=0.86):
        return "get_date"

    return None