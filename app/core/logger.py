import logging

from logging.handlers import RotatingFileHandler

from app.config import LOG_DIR


def get_logger(name: str):

    logger = logging.getLogger(name)

    if logger.handlers:

        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    )

    file_handler = RotatingFileHandler(

        LOG_DIR / "jarvis.log",

        maxBytes=5_000_000,

        backupCount=5,

        encoding="utf8"

    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    console = logging.StreamHandler()

    console.setFormatter(formatter)

    logger.addHandler(console)

    return logger