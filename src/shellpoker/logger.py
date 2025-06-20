import logging
import os

def create_logger():
    logger = logging.getLogger("shellpoker")
    logger.setLevel(os.environ.get("SHELLPOKER_LOGLEVEL", "ERROR"))
    log_enabled = os.environ.get("SHELLPOKER_LOG_TO_FILE", "false").lower() == "true"
    if log_enabled:
        handler = logging.FileHandler("shellpoker.log", encoding="utf-8")
        formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s')
        handler.setFormatter(formatter)
        if not logger.hasHandlers():
            logger.addHandler(handler)
    return logger
