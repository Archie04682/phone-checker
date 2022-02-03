import logging
from config import WRITE_LOG_TO_FILE, LOG_FILENAME, LOG_LEVEL


def get_logger():
    logger = logging.getLogger('flask-app')
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(name)s-%(levelname)s: %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if WRITE_LOG_TO_FILE:
        file_handler = logging.FileHandler(LOG_FILENAME)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(LOG_LEVEL)
    return logger
