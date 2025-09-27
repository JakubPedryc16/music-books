import logging

logger = logging.getLogger("music-books")
if not logger.hasHandlers():
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    ))
    logger.addHandler(ch)
    logger.propagate = False

logger.info("Logger Loaded Properly")
