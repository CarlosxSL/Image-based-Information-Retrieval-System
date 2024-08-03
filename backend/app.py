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
from sklearn.neighbors import NearestNeighbors

# Configuración del modelo y carga de datos
def load_models_and_data():
    # Cargar el modelo de características
    base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    model = Model(inputs=base_model.input, outputs=base_model.layers[-1].output)
    
    # Limpiar memoria
    del base_model
    tf.keras.backend.clear_session()
    
    # Cargar el modelo de vecinos más cercanos y las imágenes de entrenamiento
    model_nn = load('nearest_neighbors_model.pkl')
    train_images_flat = np.load('train_images.npy')
    
    return model, model_nn, train_images_flat

model, model_nn, train_images_flat = load_models_and_data()

def preprocess_image(image):
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
CORS(app)

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        image = request.files['image']
        img = Image.open(image)

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
