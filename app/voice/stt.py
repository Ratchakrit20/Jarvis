"""
Whisper Speech To Text Engine

Author : JarvisAI
"""

from __future__ import annotations

from pathlib import Path

import torch

from transformers import (
    AutoFeatureExtractor,
    AutoModelForSpeechSeq2Seq,
    AutoTokenizer,
    pipeline,
)

from app.config import (
    WHISPER_MODEL,
    MODEL_DIR,
    SAMPLE_RATE,
)


class WhisperSTT:
    """
    Whisper STT Engine

    Loading priority:
    1. app/models/whisper-th-small-combined
    2. Hugging Face cache แบบ offline
    3. Download from Hugging Face แล้ว save local
    """

    def __init__(self):
        self.model_name = WHISPER_MODEL
        self.local_model_dir = Path(MODEL_DIR) / "whisper-th-small-combined"

        self.use_cuda = torch.cuda.is_available()
        self.device = "cuda:0" if self.use_cuda else "cpu"
        self.device_index = 0 if self.use_cuda else -1
        self.dtype = torch.float16 if self.use_cuda else torch.float32

        print("Loading Whisper...")
        print(f"Device: {self.device}")
        print(f"Model: {self.model_name}")
        print(f"Local path: {self.local_model_dir}")

        tokenizer, feature_extractor, model = self._load_whisper()

        self.model = model.to(self.device)
        self.model.eval()

        self.pipe = pipeline(
            task="automatic-speech-recognition",
            model=self.model,
            tokenizer=tokenizer,
            feature_extractor=feature_extractor,
            torch_dtype=self.dtype,
            device=self.device_index,
        )

        print("Whisper Ready")

    def _is_local_model_ready(self) -> bool:
        """
        ตรวจว่า local model มีไฟล์หลักพอใช้หรือยัง
        """

        if not self.local_model_dir.exists():
            return False

        has_config = (self.local_model_dir / "config.json").exists()
        has_preprocessor = (self.local_model_dir / "preprocessor_config.json").exists()

        has_tokenizer = any(
            [
                (self.local_model_dir / "tokenizer.json").exists(),
                (self.local_model_dir / "tokenizer_config.json").exists(),
                (self.local_model_dir / "vocab.json").exists(),
            ]
        )

        has_model = any(
            [
                (self.local_model_dir / "model.safetensors").exists(),
                (self.local_model_dir / "pytorch_model.bin").exists(),
            ]
        )

        return has_config and has_preprocessor and has_tokenizer and has_model

    def _load_from_source(self, source: str, local_files_only: bool):
        """
        โหลด tokenizer + feature extractor + model
        ไม่ใช้ AutoProcessor เพราะบางรุ่นจะพยายามหา processor_config.json
        """

        tokenizer = AutoTokenizer.from_pretrained(
            source,
            local_files_only=local_files_only,
        )

        feature_extractor = AutoFeatureExtractor.from_pretrained(
            source,
            local_files_only=local_files_only,
        )

        try:
            model = AutoModelForSpeechSeq2Seq.from_pretrained(
                source,
                dtype=self.dtype,
                low_cpu_mem_usage=True,
                local_files_only=local_files_only,
            )
        except TypeError:
            model = AutoModelForSpeechSeq2Seq.from_pretrained(
                source,
                torch_dtype=self.dtype,
                low_cpu_mem_usage=True,
                local_files_only=local_files_only,
            )

        return tokenizer, feature_extractor, model

    def _save_local(self, tokenizer, feature_extractor, model):
        """
        Save model ลง app/models/whisper-th-small-combined
        เพื่อให้เปิด Jarvis รอบหน้าแบบ local ได้
        """

        self.local_model_dir.mkdir(parents=True, exist_ok=True)

        tokenizer.save_pretrained(str(self.local_model_dir))
        feature_extractor.save_pretrained(str(self.local_model_dir))
        model.save_pretrained(str(self.local_model_dir))

        print("Whisper saved locally")

    def _load_whisper(self):
        """
        Load Whisper แบบกันพัง:
        1. local folder
        2. Hugging Face cache offline
        3. online download
        """

        # 1. Load from app/models
        if self._is_local_model_ready():
            print("Using local Whisper model")

            return self._load_from_source(
                source=str(self.local_model_dir),
                local_files_only=True,
            )

        # 2. Try Hugging Face cache แบบ offline ก่อน
        try:
            print("Local folder incomplete. Trying Hugging Face cache...")

            tokenizer, feature_extractor, model = self._load_from_source(
                source=self.model_name,
                local_files_only=True,
            )

            print("Loaded Whisper from Hugging Face cache")

            self._save_local(
                tokenizer=tokenizer,
                feature_extractor=feature_extractor,
                model=model,
            )

            return tokenizer, feature_extractor, model

        except Exception as cache_error:
            print("No complete offline cache found")
            print("Cache reason:", cache_error)

        # 3. Download from Hugging Face
        try:
            print("Downloading Whisper from Hugging Face...")

            tokenizer, feature_extractor, model = self._load_from_source(
                source=self.model_name,
                local_files_only=False,
            )

            self._save_local(
                tokenizer=tokenizer,
                feature_extractor=feature_extractor,
                model=model,
            )

            print("Downloaded Whisper successfully")

            return tokenizer, feature_extractor, model

        except Exception as download_error:
            print()
            print("❌ Failed to load Whisper")
            print("Reason:", download_error)
            print()
            print("วิธีแก้ที่แนะนำ:")
            print("1. ลองเปลี่ยนเน็ต เช่น Hotspot มือถือ")
            print("2. ลบโฟลเดอร์ local ที่โหลดค้าง:")
            print(f"   {self.local_model_dir}")
            print("3. รันใหม่อีกครั้ง:")
            print("   python jarvis.py")
            print()

            raise

    def transcribe(self, audio):
        """
        Convert speech audio array to text
        """

        if audio is None:
            return ""

        result = self.pipe(
            {
                "sampling_rate": SAMPLE_RATE,
                "raw": audio.astype("float32"),
            },
            generate_kwargs={
                "task": "transcribe",
                "language": "th",
            },
        )

        text = result.get("text", "")

        return text.strip()