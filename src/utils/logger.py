from loguru import logger
import sys

def get_logger():
    logger.remove()
    logger.add(sys.stdout, level="INFO")
    return logger
