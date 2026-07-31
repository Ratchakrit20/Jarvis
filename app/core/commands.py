"""Pure command helpers that do not load voice or model dependencies."""

from __future__ import annotations


def should_exit(text: str) -> bool:
    """Return whether a transcript is an explicit Jarvis shutdown command."""
    if not text:
        return False

    normalized = text.strip().lower()
    non_exit_words = (
        "เปิด",
        "เปิดยูทูป",
        "เปิด youtube",
        "เปิดเพลง",
        "เปิดเว็บ",
        "เปิดโปรแกรม",
    )
    if any(word in normalized for word in non_exit_words):
        return False

    exit_phrases = (
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
    )
    return any(phrase == normalized or phrase in normalized for phrase in exit_phrases)
