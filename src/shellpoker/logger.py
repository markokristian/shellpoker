import logging

def create_logger():
    logger = logging.getLogger("shellpoker")
    logger.setLevel(logging.DEBUG)  # or DEBUG for more detail
    handler = logging.FileHandler("shellpoker.log", encoding="utf-8")
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(handler)
    return logger