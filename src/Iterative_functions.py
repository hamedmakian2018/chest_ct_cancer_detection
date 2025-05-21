import json
from pathlib import Path

from src.logger import get_logger

logger = get_logger(__name__)


def mk_dir(name):
    Dir_name = Path(name)
    try:
        Dir_name.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory created: {Dir_name}")
    except Exception as e:
        logger.error(f"Error creating directory {Dir_name}: {e}")
    return Dir_name


def save_json(path, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"json file saved at: {path}")
