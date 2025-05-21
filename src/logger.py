import logging
import sys
from datetime import datetime
from pathlib import Path

LOG_DIR_NAME = "logs"

LOG_DIR = Path(LOG_DIR_NAME)

LOG_DIR.mkdir(parents=True, exist_ok=True)
print(f"Directory created: {LOG_DIR}")

LOG_FILE = LOG_DIR / f"log_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"

log_format = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)],
)


def get_logger(name):
    return logging.getLogger(name)
