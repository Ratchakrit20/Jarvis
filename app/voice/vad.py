"""
Voice Activity Detection

Author : JarvisAI

หน้าที่:
- รอฟังเสียงจากไมค์
- เริ่มอัดเมื่อมีเสียงพูด
- หยุดอัดเมื่อผู้ใช้เงียบ
- ส่ง numpy audio array กลับไปให้ Whisper
"""

from __future__ import annotations

import time
from typing import Optional

import numpy as np
import sounddevice as sd

from app.config import SAMPLE_RATE


class VoiceActivityRecorder:
    """
    Simple Energy-Based VAD

    เหมาะกับ Phase 1:
    - ไม่ต้องลง model เพิ่ม
    - ใช้ได้กับภาษาไทย/อังกฤษ
    - ใช้ตรวจว่ามีเสียงพูดหรือไม่มีเสียงพูด
    """

    def __init__(
        self,
        sample_rate: int = SAMPLE_RATE,
        block_duration: float = 0.03,
        start_threshold: float = 0.012, # ระดับเสียงที่ถือว่าเริ่มพูด
        stop_threshold: float = 0.008, # ระดับเสียงที่ถือว่าเงียบ
        silence_duration: float = 1.0, # เงียบต่อเนื่องกี่วิถึงจะหยุดอัด
        max_record_seconds: float = 15.0, # กันอัดยาวเกิน
        min_record_seconds: float = 0.4, # กันเสียงสั้นเกิน
        pre_speech_seconds: float = 0.3, # เก็บเสียงก่อนเริ่มพูดเล็กน้อย
    ):
        self.sample_rate = sample_rate

        # ขนาด block ต่อรอบ เช่น 0.03 วิ = 30ms
        self.block_duration = block_duration
        self.block_size = int(sample_rate * block_duration)

        # ระดับเสียงที่ถือว่าเริ่มพูด
        self.start_threshold = start_threshold

        # ระดับเสียงที่ถือว่าเงียบ
        self.stop_threshold = stop_threshold

        # เงียบต่อเนื่องกี่วิถึงจะหยุดอัด
        self.silence_duration = silence_duration

        # กันอัดยาวเกิน
        self.max_record_seconds = max_record_seconds

        # กันเสียงสั้นเกิน เช่น คลิก/กระแทก
        self.min_record_seconds = min_record_seconds

        # เก็บเสียงก่อนเริ่มพูดเล็กน้อย กันหัวคำหาย
        self.pre_speech_seconds = pre_speech_seconds
        self.pre_speech_blocks = max(
            1,
            int(pre_speech_seconds / block_duration),
        )

    def _rms(self, audio_block: np.ndarray) -> float:
        """
        คำนวณระดับพลังงานเสียงแบบ RMS
        """

        if audio_block is None or len(audio_block) == 0:
            return 0.0

        audio_block = audio_block.astype(np.float32)

        return float(np.sqrt(np.mean(np.square(audio_block))))

    def listen(self) -> Optional[np.ndarray]:
        """
        รอฟังจนกว่าจะมีเสียงพูด
        จากนั้นอัดต่อจนผู้ใช้หยุดพูด

        Return:
            np.ndarray audio float32 mono 16k
        """

        print("🎧 Jarvis กำลังฟัง... พูดได้เลย")

        pre_buffer: list[np.ndarray] = []
        recorded_blocks: list[np.ndarray] = []

        is_recording = False
        speech_started_at: Optional[float] = None
        last_voice_at: Optional[float] = None

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            blocksize=self.block_size,
        ) as stream:

            while True:
                block, overflowed = stream.read(self.block_size)

                if overflowed:
                    print("⚠️ Audio input overflow")

                # block shape: (n, 1) -> (n,)
                block = block.reshape(-1)

                energy = self._rms(block)
                now = time.time()

                # เก็บ pre-buffer ตลอดตอนยังไม่เริ่มอัด
                if not is_recording:
                    pre_buffer.append(block.copy())

                    if len(pre_buffer) > self.pre_speech_blocks:
                        pre_buffer.pop(0)

                # ยังไม่เริ่มอัด รอเสียงเกิน threshold
                if not is_recording:
                    if energy >= self.start_threshold:
                        is_recording = True
                        speech_started_at = now
                        last_voice_at = now

                        recorded_blocks.extend(pre_buffer)
                        recorded_blocks.append(block.copy())

                        print("🎙️ ได้ยินเสียงแล้ว กำลังอัด...")

                    continue

                # กำลังอัดอยู่
                recorded_blocks.append(block.copy())

                if energy >= self.stop_threshold:
                    last_voice_at = now

                record_duration = now - speech_started_at if speech_started_at else 0
                silence_time = now - last_voice_at if last_voice_at else 0

                # หยุดเมื่อเงียบพอ และอัดมานานเกินขั้นต่ำ
                if (
                    silence_time >= self.silence_duration
                    and record_duration >= self.min_record_seconds
                ):
                    print("🛑 หยุดพูดแล้ว ส่งเข้า Whisper")
                    break

                # กันไม่ให้อัดยาวเกิน
                if record_duration >= self.max_record_seconds:
                    print("⏱️ อัดถึงเวลาสูงสุดแล้ว ส่งเข้า Whisper")
                    break

        if not recorded_blocks:
            return None

        audio = np.concatenate(recorded_blocks).astype(np.float32)

        # กันเสียงเบา/สั้นผิดปกติ
        if len(audio) < int(self.sample_rate * self.min_record_seconds):
            print("⚠️ เสียงสั้นเกินไป ข้าม")
            return None

        return audio