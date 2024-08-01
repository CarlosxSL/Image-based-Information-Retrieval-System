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
from sklearn.neighbors import NearestNeighbors  # Asegúrate de importar esto si estás usando k-NN

# Cargar el modelo de características
base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model = Model(inputs=base_model.input, outputs=base_model.layers[-1].output)

# Cargar el modelo de vecinos más cercanos y las imágenes de entrenamiento
model_nn = load('nearest_neighbors_model.pkl')  # Ajusta el nombre y la ruta según corresponda
train_images_flat = np.load('train_images.npy')  # Ajusta el nombre y la ruta según corresponda

def preprocess_image(image):
    # Convertir la imagen a RGB y redimensionar a 224x224
    image = image.convert('RGB').resize((224, 224))
    image_array = np.array(image) / 255.0
    return tf.convert_to_tensor(image_array, dtype=tf.float32)

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def get_image_from_flat_array(index):
    img_array = train_images_flat[index]
    return Image.fromarray((img_array * 255).astype(np.uint8))

app = Flask(__name__)
CORS(app)  # Permite solicitudes desde cualquier origen

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        image = request.files['image']
        img = Image.open(image)

        # Redimensionar la imagen para mejorar el rendimiento
        max_dimension = 1024
        img.thumbnail((max_dimension, max_dimension))

        # Convertir la imagen subida a base64
        img_uploaded_base64 = image_to_base64(img)

        # Preprocesar la imagen
        img_preprocessed = preprocess_image(img)
        img_preprocessed = tf.expand_dims(img_preprocessed, axis=0)
        features = model.predict(img_preprocessed).flatten().reshape(1, -1)

        # Predicción
        distances, indices = model_nn.kneighbors(features)

        # Obtener las 5 imágenes más cercanas
        closest_images = [image_to_base64(get_image_from_flat_array(idx)) for idx in indices[0]]

        return jsonify({
            'closest_images': closest_images,
            'uploaded_image': img_uploaded_base64
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
