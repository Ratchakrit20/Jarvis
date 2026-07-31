from enum import Enum


class Event(Enum):

    WAKE_WORD = "wake_word"

    SPEECH_RECOGNIZED = "speech_recognized"

    TOOL_CALLED = "tool_called"

    TOOL_FINISHED = "tool_finished"

    LLM_START = "llm_start"

    LLM_FINISH = "llm_finish"

    TTS_START = "tts_start"

    TTS_FINISH = "tts_finish"

    SYSTEM_ERROR = "system_error"

    USER_ERROR = "user_error"