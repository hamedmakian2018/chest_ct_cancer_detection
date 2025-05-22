import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


from src.config_reader import read_config
from src.data_ingestion import DataIngestion

config = read_config("./config/config.yaml")


data_ingestion = DataIngestion(config)
data_ingestion.download_unzip_file()
