import logging

logger = logging.getLogger("music-books")
if not logger.hasHandlers():
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  
    ch.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    ))
    logger.addHandler(ch)
    logger.propagate = False

logger.debug("Logger loaded properly (DEBUG)")
logger.info("Logger loaded properly (INFO)")
