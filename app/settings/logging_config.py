import logging
from logging.handlers import RotatingFileHandler

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "./app/settings/app.log"

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10_000_000, backupCount=5)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(level=logging.INFO, handlers=[file_handler])

logger = logging.getLogger("FastAPI")
