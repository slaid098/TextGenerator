from pathlib import Path

from loguru import logger


def set_logger() -> None:
    path = Path("logs.log")
    logger.add(path, format="{time} {level} {message}", colorize=True,
               level="INFO", rotation="5 MB", compression="zip")
