import logging


def get_logger():
    logger = logging.getLogger('flask-app')
    # file_handler = logging.FileHandler("flask-app-log.txt")
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(name)s-%(levelname)s: %(message)s')
    # file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
    return logger
