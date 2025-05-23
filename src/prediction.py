import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


import os
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

from src.config_reader import read_config


class Prediction:
    def __init__(self, config, filename):
        self.filename = filename
        self.config = config
        # self.data_ingestion = self.config.data_ingestion
        # self.data_processing = self.config.data_processing
        # self.directories = self.config.directories
        self.files = self.config.files
        # self.training = self.config.training

        self.trained_model_file = self.files.trained_model_file

        # self.image_size = self.data_processing.image_size
        # self.batch_size = self.data_processing.batch_size
        # self.classes = self.data_processing.classes

    def prdict(self):
        # load model
        self.model = tf.keras.models.load_model(self.trained_model_file)

        imagename = self.filename
        test_image = image.load_img(imagename, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = test_image / 255.0
        test_image = np.expand_dims(test_image, axis=0)
        result = np.argmax(self.model.predict(test_image), axis=1)
        print(result)
        if result[0] == 1:
            prediction = "Normal"
            print(prediction)
            return [{"image": prediction}]
        else:
            prediction = "Adenocarcinoma Cancer"
            print(prediction)
            return [{"image": prediction}]


"""
# test
if __name__ == "__main__":
    test_image = r"C:\Learning\chest_ct_cancer_detection\artifacts\raw\Chest-CT-Scan-data\normal\13 - Copy - Copy.png"  # مسیر عکس تست
    test_image_1= r"C:\Learning\chest_ct_cancer_detection\artifacts\raw\Chest-CT-Scan-data\adenocarcinoma\000005 (9).png"
    config = read_config("./config/config.yaml")
    print("Normal result prediction is: ")
    pre = Prediction(config,test_image)
    pre.prdict()

    print("Canceric result prediction is: ")
    pre1 = Prediction(config,test_image_1)
    pre1.prdict()

"""
