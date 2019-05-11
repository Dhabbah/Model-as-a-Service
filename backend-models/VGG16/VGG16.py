import sys
import os
import numpy as np

# Keras
from keras.preprocessing import image

# Flask utils
from flask import Flask, request
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer
from flask_cors import CORS, cross_origin

# Define a flask app
application = Flask(__name__)
CORS(application, support_credentials=True)
application.secret_key="VGG16"

from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
model = VGG16(weights='imagenet')
print('The model VGG16 loaded')
print('Check http://127.0.0.1:64005/')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img) # Preprocessing the image
    x = np.expand_dims(x, axis=0) # x = np.true_divide(x, 255)

    preds = model.predict(preprocess_input(x))
    return preds

#@app.after_request
#def after_request(response):
#  response.headers.add('Access-Control-Allow-Origin', '*')
#  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#  return response

@application.route('/VGG16')
@cross_origin(supports_credentials=True)
def index():
 return "VGG16 Model"

@application.route('/VGG16/predict', methods=['POST'])
@cross_origin(supports_credentials=True)
def upload():
    #body = request.body
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        pred_class = decode_predictions(preds, top=5)   # ImageNet Decode
        result = str(pred_class[0][0][1])               # Convert to string
        return 'The model VGG16 predicts this image as : ' + result
    return None


if __name__ == '__main__':

    # Serve the app with gevent
    #http_server = WSGIServer(('', 64005), app)
    #http_server.serve_forever()
	application.run(host='127.0.0.1', port=64005)