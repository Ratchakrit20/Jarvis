import torch
import sounddevice as sd
from transformers import AutoTokenizer, VitsModel
from .processor import clean_text


MODEL = "facebook/mms-tts-tha"


class MMSTTS:

    def __init__(self):

        self.model = VitsModel.from_pretrained(MODEL)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)

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