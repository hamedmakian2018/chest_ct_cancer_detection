from src.config_reader import read_config
from src.data_processing import DataProcessing

config = read_config("./config/config.yaml")


data_processing = DataProcessing(config)
data_processing.get_base_model()

data_processing.update_base_model()
