"""Download the models required by Jarvis into reproducible local locations."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from transformers import AutoFeatureExtractor, AutoModelForSpeechSeq2Seq, AutoTokenizer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WHISPER_REPO = "biodatlab/whisper-th-small-combined"
WHISPER_DIR = PROJECT_ROOT / "app" / "models" / "whisper-th-small-combined"
OLLAMA_MODEL = "qwen3:8b"


def download_whisper() -> None:
    """Download and save the Thai Whisper assets excluded from Git."""
    WHISPER_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {WHISPER_REPO} to {WHISPER_DIR}")

    tokenizer = AutoTokenizer.from_pretrained(WHISPER_REPO)
    feature_extractor = AutoFeatureExtractor.from_pretrained(WHISPER_REPO)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(WHISPER_REPO)

    tokenizer.save_pretrained(WHISPER_DIR)
    feature_extractor.save_pretrained(WHISPER_DIR)
    model.save_pretrained(WHISPER_DIR)
    print("Whisper model is ready.")


def download_ollama() -> None:
    """Ask the local Ollama installation to download the configured LLM."""
    print(f"Pulling Ollama model {OLLAMA_MODEL}")
    try:
        subprocess.run(["ollama", "pull", OLLAMA_MODEL], check=True)
    except FileNotFoundError as exc:
        raise SystemExit(
            "Ollama was not found. Install it from https://ollama.com/download first."
        ) from exc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-whisper", action="store_true")
    parser.add_argument("--skip-ollama", action="store_true")
    args = parser.parse_args()

    if not args.skip_whisper:
        download_whisper()
    if not args.skip_ollama:
        download_ollama()


if __name__ == "__main__":
    main()
