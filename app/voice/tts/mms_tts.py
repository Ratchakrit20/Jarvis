import torch
import sounddevice as sd
from transformers import AutoTokenizer, VitsModel
from app.config import TTS_MODEL
from .processor import clean_text


class MMSTTS:

    def __init__(self):

        self.model = VitsModel.from_pretrained(TTS_MODEL)
        self.tokenizer = AutoTokenizer.from_pretrained(TTS_MODEL)

    def speak(self, text: str):

        text = clean_text(text)

        inputs = self.tokenizer(text, return_tensors="pt")

        with torch.no_grad():
            waveform = self.model(**inputs).waveform

        audio = waveform.squeeze().cpu().numpy()

        # normalize (ช่วยลดเสียงแข็ง)
        audio = audio / max(0.01, abs(audio).max())

        sd.play(audio, 16000)
        sd.wait()
