import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


from pathlib import Path

import uvicorn
from fastapi import FastAPI
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

from src.config_reader import read_config
from src.Iterative_functions import decodeImage
from src.prediction import Prediction

"""

config = read_config("./config/config.yaml")

app = Flask(__name__)
CORS(app)

class Clientapp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.clssifier = Prediction(config, self.filename)
@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/train", methods=['GET','POST'])
@cross_origin()
def trainRoute():
    #os.system("python -m pipeline.run")
    os.system("dvc repro")
    return "Training done successfully!"


@app.route("/prediction", methods=['POST'])
@cross_origin()
def predictRoute():
    image = request.json['image']
    decodeImage(image, clApp.filename)
    result = clApp.clssifier.predict()
    return jsonify(result)


if __name__== "__main__":
    clApp = Clientapp()
    app.run(host="0.0.0.0", port=8080)




"""

import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from pathlib import Path

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin

from src.config_reader import read_config
from src.Iterative_functions import decodeImage
from src.prediction import Prediction

# Read config
config = read_config("./config/config.yaml")

# Flask setup
app = Flask(__name__)
CORS(app)


class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = Prediction(config, self.filename)


# Initialize ClientApp (IMPORTANT: it must happen before usage)
clApp = ClientApp()


@app.route("/", methods=["GET"])
@cross_origin()
def home():
    return render_template("index.html")


@app.route("/train", methods=["GET", "POST"])
@cross_origin()
def trainRoute():
    os.system("dvc repro")  # Or replace with pipeline call
    # return "Training done successfully!"
    return jsonify({"message": "Training done"})


@app.route("/predict", methods=["POST"])
@cross_origin()
def predictRoute():
    try:
        image_data = request.json["image"]
        decodeImage(image_data, clApp.filename)  # Saves image as 'inputImage.jpg'
        result = clApp.classifier.prdict()  # Use the working prediction method
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
