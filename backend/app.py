from flask import Flask, request, jsonify
from flask_cors import CORS
from joblib import load
import numpy as np
from PIL import Image
import io
import base64
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.models import Model
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Variables globales para modelos y datos
model = None
model_nn = None
collection = None

def initialize():
    global model, model_nn, collection
    # Cargar el modelo de características
    base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    model = Model(inputs=base_model.input, outputs=base_model.layers[-1].output)
    
    # Limpiar memoria
    del base_model
    tf.keras.backend.clear_session()
    
    # Cargar el modelo de vecinos más cercanos
    model_nn = load('nearest_neighbors_model.pkl')
    
    # Conectar a MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['caltech101db']
    collection = db['images']

initialize()

def preprocess_image(image):
    image = tf.image.resize(image, (224, 224))  # Redimensiona la imagen
    image = tf.cast(image, tf.float32) / 255.0  # Normaliza la imagen
    return image

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def get_image_from_db(index):
    image_doc = collection.find_one({'index': index}, {'_id': 0, 'image': 1})
    if image_doc:
        return Image.open(io.BytesIO(image_doc['image']))
    return None

@app.route('/api/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    try:
        image = request.files['image']
        img = Image.open(image)
        img_uploaded_base64 = image_to_base64(img)

        img_preprocessed = preprocess_image(tf.convert_to_tensor(np.array(img)))
        img_preprocessed = tf.expand_dims(img_preprocessed, axis=0)        

        query_features = model.predict(img_preprocessed).flatten().reshape(1, -1)

        distances, indices = model_nn.kneighbors(query_features, n_neighbors=10)
        # print(indices[0])
        
        closest_images = [image_to_base64(get_image_from_db(int(index))) for index in indices[0] if get_image_from_db(int(index))]

        return jsonify({
            'closest_images': closest_images,
            'uploaded_image': img_uploaded_base64
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)