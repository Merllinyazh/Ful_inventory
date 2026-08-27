import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("inventory_logger")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler("app.log", maxBytes=50 * 1024 * 1024, backupCount=5)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)