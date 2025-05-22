from src.config_reader import read_config
from src.model_training import Training

config = read_config("./config/config.yaml")


data_training = Training(config)

data_training.get_updated_model()
data_training.train_valid_generator()
data_training.train()
