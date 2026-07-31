# memory/memory.py

class Memory:
    def __init__(self):
        self.history = []

    def add_user(self, text: str):
        self.history.append({"role": "user", "content": text})

    def add_assistant(self, text: str):
        self.history.append({"role": "assistant", "content": text})

    def get(self, limit: int = 10):
        return self.history[-limit:]