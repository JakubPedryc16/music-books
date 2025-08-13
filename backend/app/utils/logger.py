import logging

logger = logging.getLogger("music-books")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))

logger.addHandler(console_handler)
logger.propagate = False 