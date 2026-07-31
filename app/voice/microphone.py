"""
voice/microphone.py

Microphone Recorder for JarvisAI

- Record microphone audio
- Auto stop after silence
- Return numpy array (float32)
"""

from __future__ import annotations

import queue
import time

import numpy as np
import sounddevice as sd


class Microphone:
    """
    Record audio from microphone.

    Returns
    -------
    numpy.ndarray
        Audio samples (float32)
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        silence_threshold: float = 0.01,
        silence_duration: float = 1.0,
        max_record_time: int = 15,
    ) -> None:

        self.sample_rate = sample_rate
        self.channels = channels

        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.max_record_time = max_record_time

        self._queue: queue.Queue[np.ndarray] = queue.Queue()

    def _callback(self, indata, frames, time_info, status):

        if status:
            print(status)

        self._queue.put(indata.copy())

    def record(self) -> np.ndarray:
        """
        Start recording.

        Wait until user speaks.

        Stop after silence.

        Returns
        -------
        numpy.ndarray
        """

        print("🎤 Listening...")

        frames = []

        speech_started = False

        silence_count = 0

        required_silence = int(
            self.silence_duration
            * self.sample_rate
            / 1024
        )

        start_time = time.time()

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            blocksize=1024,
            dtype="float32",
            callback=self._callback,
        ):

            while True:

                if time.time() - start_time > self.max_record_time:
                    break

                data = self._queue.get()

                volume = np.abs(data).mean()

                if not speech_started:

                    if volume > self.silence_threshold:

                        speech_started = True

                        print("🗣️ Speech detected")

                        frames.append(data)

                    continue

                frames.append(data)

                if volume < self.silence_threshold:

                    silence_count += 1

                else:

                    silence_count = 0

                if silence_count >= required_silence:

                    break

        if len(frames) == 0:

            return np.array([], dtype=np.float32)

        audio = np.concatenate(frames, axis=0)

        return audio.squeeze().astype(np.float32)


if __name__ == "__main__":

    mic = Microphone()

    audio = mic.record()

    print(audio.shape)

    print(audio.dtype)