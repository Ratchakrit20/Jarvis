import sounddevice as sd

def record_audio(seconds=5, fs=16000):

    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()

    return audio.flatten().astype("float32")