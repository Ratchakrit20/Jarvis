from pathlib import Path

# ============================
# Project
# ============================

PROJECT_NAME = "Jarvis AI"

VERSION = "1.0.0"

BASE_DIR = Path(__file__).resolve().parent

# ============================
# Folder
# ============================

LOG_DIR = BASE_DIR / "logs"
MODEL_DIR = BASE_DIR / "models"
MEMORY_DIR = BASE_DIR / "memory"

LOG_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)
MEMORY_DIR.mkdir(exist_ok=True)

# ============================
# Language
# ============================

LANGUAGE = "th"

# ============================
# Whisper
# ============================

WHISPER_MODEL = "biodatlab/whisper-th-small-combined"

# ============================
# TTS
# ============================

TTS_MODEL = "facebook/mms-tts-tha"

# ============================
# Ollama
# ============================

OLLAMA_HOST = "http://localhost:11434"

# LLM_MODEL = "qwen2.5:7b"
LLM_MODEL = "qwen3:8b"
# ============================
# Audio
# ============================

SAMPLE_RATE = 16000

MIC_TIMEOUT = 5

PHRASE_TIME_LIMIT = 10

# ============================
# Wake Word
# ============================

WAKE_WORD = "จาร์วิส"

# ============================
# Debug
# ============================

DEBUG = True