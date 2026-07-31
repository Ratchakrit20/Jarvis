from enum import Enum


class State(Enum):

    IDLE = "idle"

    LISTENING = "listening"

    THINKING = "thinking"

    RESPONDING = "responding"

    ERROR = "error"

    EXIT = "exit"