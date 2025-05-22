from src.config_reader import read_config
from src.model_evaluation_mlflow import Evaluation

config = read_config("./config/config.yaml")


data_evaluation = Evaluation(config)
data_evaluation.evaluation()
data_evaluation.log_into_mlflow()
