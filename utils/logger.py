from loguru import logger
import sys


def setup_logger():

    logger.remove()

    logger.add(
        sys.stdout,
        format="<green>{time}</green> | <level>{level}</level> | {message}",
        level="INFO"
    )

    logger.add(
        "logs/system.log",
        rotation="10 MB",
        retention="10 days",
        level="DEBUG"
    )

    return logger


log = setup_logger()