from pathlib import Path

import yaml
from box import ConfigBox

from src.logger import get_logger

logger = get_logger(__name__)


def read_config(config_path):
    config_file = Path(config_path)
    if not config_file.exists():
        logger.erreor(f"Config file not found at {config_path}")
        raise FileNotFoundError(f"Config file not found at {config_path}")
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            return ConfigBox(config)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {config_file}")
        raise e
