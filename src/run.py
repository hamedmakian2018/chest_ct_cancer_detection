import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


from logger import get_logger

logger = get_logger(__name__)
# logger.info("Just for test")
# logger.error("again just for test")


from src.config_reader import read_config
from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessing
from src.model_evaluation_mlflow import Evaluation
from src.model_training import Training

config = read_config("./config/config.yaml")


data_ingestion = DataIngestion(config)
data_ingestion.download_unzip_file()


data_processing = DataProcessing(config)
data_processing.get_base_model()

# data_processing.prepare_full_model()
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


data_training = Training(config)

data_training.get_updated_model()
data_training.train_valid_generator()
data_training.train()


data_evaluation = Evaluation(config)
data_evaluation.evaluation()
data_evaluation.log_into_mlflow()
