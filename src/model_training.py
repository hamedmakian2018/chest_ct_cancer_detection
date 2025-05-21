import tensorflow as tf

from src.Iterative_functions import mk_dir
from src.logger import get_logger

"""
print("Before enabling eager:", tf.executing_eagerly())

tf.data.experimental.enable_debug_mode()
print("code1: Eager execution enabled:", tf.executing_eagerly())
tf.config.run_functions_eagerly(True)
print("code2: Eager execution enabled:", tf.executing_eagerly())

"""


logger = get_logger(__name__)


class Training:
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

    def get_updated_model(self):
        updated_model = self.updated_base_model_file
        self.model = tf.keras.models.load_model(updated_model)

        self.model.compile(
            optimizer=tf.keras.optimizers.SGD(learning_rate=self.learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=[
                "accuracy",
                tf.keras.metrics.Precision(),
                tf.keras.metrics.Recall(),
            ],
        )

    def train_valid_generator(self):

        data_generator_kwargs = dict(rescale=1.0 / 255, validation_split=0.2)

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
        if self.augmentation:
            train_generator = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range=40,
                horizontal_flip=True,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                **data_generator_kwargs,
            )
        else:
            train_generator = valid_data_generator

        self.train_generator = train_generator.flow_from_directory(
            directory=self.training_data_dir,
            subset="training",
            shuffle=False,
            **data_flow_kwargs,
        )

    @staticmethod
    def save_model(Path, model: tf.keras.Model):
        model.save(Path)
        logger.info(f"Trained Model saved at: {Path}")

    def train(self):

        self.step_per_epoch = (
            self.train_generator.samples // self.train_generator.batch_size
        )
        self.validation_steps = (
            self.valid_generator.samples // self.valid_generator.batch_size
        )

        self.model.fit(
            self.train_generator,
            epochs=self.epoch,
            steps_per_epoch=self.step_per_epoch,
            validation_steps=self.validation_steps,
            validation_data=self.valid_generator,
        )

        self.save_model(Path=self.trained_model_file, model=self.model)
