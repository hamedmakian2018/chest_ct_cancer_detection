import tensorflow as tf

from src.Iterative_functions import mk_dir
from src.logger import get_logger

logger = get_logger(__name__)


class DataProcessing:
    def __init__(self, config):

        self.config = config
        self.data_ingestion = self.config.data_ingestion
        self.data_processing = self.config.data_processing
        self.directories = self.config.directories
        self.files = self.config.files

        self.base_model_file = self.files.base_model_file
        self.updated_base_model_file = self.files.updated_base_model_file

        self.image_size = self.data_processing.image_size
        self.include_top = self.data_processing.include_top
        self.classes = self.data_processing.classes
        self.weights = config.data_processing.weights
        self.learning_rate = self.data_processing.learning_rate

    def get_base_model(self):

        # logger.info(f"Folder name {self.PROCESSING_DIR} was created")
        base_model = self.base_model_file
        self.model = tf.keras.applications.vgg16.VGG16(
            input_shape=self.image_size,
            weights=self.weights,
            include_top=self.include_top,
        )

        self.save_model(Path=base_model, model=self.model)
        logger.info(f"The basic model VGG16 was saved in {base_model}")

    def prepare_full_model(
        self, model, classes, freeze_all, freeze_till, learning_rate
    ):

        logger.info(f"Starting to prepare full model")

        # Freeze layers based on the provided parameters
        if freeze_all:
            for layer in model.layers:
                layer.trainable = False

        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model.layers[:freeze_till]:
                layer.trainable = False

        # Add classification head
        flatten_in = tf.keras.layers.Flatten()(model.output)
        prediction = tf.keras.layers.Dense(units=classes, activation="softmax")(
            flatten_in
        )

        # Build the full model
        full_model = tf.keras.models.Model(inputs=model.input, outputs=prediction)

        # Compile the full model
        full_model.compile(
            optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"],
        )
        full_model.summary()

        """

        trainable_count = 0  

        for layer in full_model.layers:

            num_params = layer.count_params()
            print(f"Layer: {layer.name}, Trainable: {layer.trainable}, Parameters: {num_params}")
            

            if layer.trainable and num_params > 0:
                trainable_count += 1

        print(f"\nNumber of truly trainable layers: {trainable_count}")

        return full_model
        """

        return full_model

    def update_base_model(self):

        self.full_model = self.prepare_full_model(
            model=self.model,
            classes=self.classes,
            freeze_all=True,
            freeze_till=None,
            learning_rate=self.learning_rate,
        )
        updated_base_model = self.updated_base_model_file

        self.save_model(Path=updated_base_model, model=self.full_model)
        logger.info(f"The full model VGG16 was saved in {updated_base_model}")

    def save_model(self, Path: str, model):
        model.save(Path)
        logger.info(f"Model saved at: {Path}")
