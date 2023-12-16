import sys
from loguru import logger
from app.config import AppSettings


def setup_logging(settings: AppSettings) -> None:
    """
    Setup logging
    :return: None
    """
    log_format: str = '<green>{time}</green> <level>{level}</level>'
    log_level: str = 'TRACE' if settings.debug else 'INFO'

    if settings.debug:
        log_format += ' <cyan>{module}.{name}:{function}:{line}</cyan>'

    log_format += ' <level>{message}</level>'
    logger.remove()
    logger.add(sys.stderr, colorize=True, format=log_format, level=log_level)
