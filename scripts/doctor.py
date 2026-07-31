"""Run lightweight checks after cloning JarvisAI."""

from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "app" / "models" / "whisper-th-small-combined"
MODEL_FILES = {
    "config.json",
    "generation_config.json",
    "model.safetensors",
    "preprocessor_config.json",
    "tokenizer.json",
    "tokenizer_config.json",
}
IMPORTS = {
    "accelerate": "accelerate",
    "edge-tts": "edge_tts",
    "numpy": "numpy",
    "ollama": "ollama",
    "pygame": "pygame",
    "sounddevice": "sounddevice",
    "soundfile": "soundfile",
    "torch": "torch",
    "transformers": "transformers",
}


def report(ok: bool, label: str, detail: str = "") -> bool:
    marker = "OK" if ok else "FAIL"
    suffix = f" - {detail}" if detail else ""
    print(f"[{marker}] {label}{suffix}")
    return ok


def main() -> int:
    checks: list[bool] = []
    checks.append(report(sys.version_info[:2] == (3, 11), "Python 3.11", sys.version.split()[0]))

    for package, module in IMPORTS.items():
        installed = importlib.util.find_spec(module) is not None
        checks.append(report(installed, f"Python package: {package}"))

    missing_model_files = sorted(
        name for name in MODEL_FILES if not (MODEL_DIR / name).is_file()
    )
    checks.append(
        report(
            not missing_model_files,
            "Local Whisper model",
            "missing: " + ", ".join(missing_model_files) if missing_model_files else str(MODEL_DIR),
        )
    )
    checks.append(report(shutil.which("ollama") is not None, "Ollama command"))

    print()
    if all(checks):
        print("JarvisAI prerequisites look ready.")
        return 0

    print("Some prerequisites are missing. Follow SETUP.md, then run this check again.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
