import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

"""

from logger import get_logger

logger = get_logger(__name__)
#logger.info("Just for test")
#logger.error("again just for test")


from config_reader import read_config

config= read_config('./config/config.yaml')
data= config.data_ingestion.artifact_dir
print(data)

"""


from src.config_reader import read_config
from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessing

config = read_config("./config/config.yaml")
data_ingestion = DataIngestion(config)
data_ingestion.download_unzip_file()


data_processing = DataProcessing(config)
data_processing.get_base_model()
data_processing.prepare_full_model()
data_processing.update_base_model()


trainable_count = sum(
    1
    for layer in data_processing.full_model.layers
    if layer.trainable and layer.count_params() > 0
)
print(f"The number of truly trainable layers: {trainable_count}")

"""
for layer in data_processing.full_model.layers:
    print(f"Layer: {layer.name}, Trainable: {layer.trainable}, Parameters: {layer.count_params()}")

"""
