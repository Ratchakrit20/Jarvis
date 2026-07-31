class JarvisError(Exception):
    """Base Exception"""


class SystemError(JarvisError):
    pass


class NetworkError(SystemError):
    pass


class STTError(SystemError):
    pass


class TTSError(SystemError):
    pass


class LLMError(SystemError):
    pass


class WakeWordError(SystemError):
    pass


class ToolError(SystemError):
    pass


class UserInputError(JarvisError):
    pass