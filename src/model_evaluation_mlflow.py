from pathlib import Path

import mlflow
import tensorflow as tf

from Iterative_functions import save_json
from src.logger import get_logger

"""
print("Before enabling eager:", tf.executing_eagerly())

tf.data.experimental.enable_debug_mode()
print("code1: Eager execution enabled:", tf.executing_eagerly())
tf.config.run_functions_eagerly(True)
print("code2: Eager execution enabled:", tf.executing_eagerly())

"""


logger = get_logger(__name__)


class Evaluation:
    def __init__(self, config):
        self.config = config
        self.data_ingestion = self.config.data_ingestion
        self.data_processing = self.config.data_processing
        self.directories = self.config.directories
        self.files = self.config.files
        self.training = self.config.training

        self.base_model_file = self.files.base_model_file
        self.updated_base_model_file = self.files.updated_base_model_file

        self.trained_model_file = self.files.trained_model_file

        self.image_size = self.data_processing.image_size
        self.batch_size = self.data_processing.batch_size
        self.include_top = self.data_processing.include_top
        self.epoch = self.data_processing.epoch
        self.classes = self.data_processing.classes
        self.weights = config.data_processing.weights
        self.learning_rate = self.data_processing.learning_rate
        self.augmentation = self.data_processing.augmentation

        self.training_data_dir = self.training.training_data_dir

    def _valid_generator(self):

        data_generator_kwargs = dict(rescale=1.0 / 255, validation_split=0.3)

        data_flow_kwargs = dict(
            target_size=self.image_size[:-1],
            batch_size=self.batch_size,
            interpolation="bilinear",
        )

        valid_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
            **data_generator_kwargs
        )

        self.valid_generator = valid_data_generator.flow_from_directory(
            directory=self.training_data_dir,
            subset="validation",
            shuffle=False,
            **data_flow_kwargs,
        )

    @staticmethod
    def load_model(path):
        return tf.keras.models.load_model(path)

    """
        self.model.compile(
            optimizer=tf.keras.optimizers.SGD(learning_rate=self.learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy", tf.keras.metrics.Precision(), tf.keras.metrics.Recall()],
        )
    """

    def evaluation(self):
        self.model = self.load_model(self.trained_model_file)
        self._valid_generator()
        self.score = self.model.evaluate(self.valid_generator)
        self.save_score()

    def save_score(self):
        scores = {
            "loss": self.score[0],
            "accuracy": self.score[1],
            "precision": self.score[2],
            "recall": self.score[3],
        }
        save_json(path=Path("scores.json"), data=scores)
        logger.info("Evaluation scores saved successfully.")

    def log_into_mlflow(self):
        mlflow.set_experiment("CHEST CT CANCER DETECTION")
        with mlflow.start_run():
            logger.info(f"MLflow started")
            mlflow.set_tag("model type", "VGG16")
            mlflow.log_params(self.data_processing)
            mlflow.log_metrics(
                {
                    "loss": self.score[0],
                    "accuracy": self.score[1],
                    "precision": self.score[2],
                    "recall": self.score[3],
                }
            )
            mlflow.keras.log_model(
                self.model, "model", registered_model_name="VGG16Model"
            )
