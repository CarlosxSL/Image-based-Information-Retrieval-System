"use client";

import { useState } from 'react';
import axios from 'axios';
import '../../public/styles.css'; // Importa el archivo CSS

const HomePage = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [similarImages, setSimilarImages] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedImage(file);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!selectedImage) {
      setError("Por favor, seleccione una imagen.");
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setUploadedImage(response.data.uploaded_image);
      setSimilarImages(response.data.closest_images);
      setError(null);
    } catch (error) {
      setError('Error enviando la imagen: ' + (error as Error).message);
      setUploadedImage(null);
      setSimilarImages([]);
    }
  };

  return (
    <div>
      <h1>SRI basado en IMÁGENES</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="image">Seleccione una imagen:</label>
        <input
          type="file"
          name="image"
          id="image"
          accept="image/*"
          onChange={handleFileChange}
          required
        />
        <button type="submit">Enviar</button>
      </form>

      {error && <p>{error}</p>}

      {uploadedImage && (
        <div>
          <h2>Imagen Subida:</h2>
          <img src={`data:image/png;base64,${uploadedImage}`} alt="Imagen Subida" />
        </div>
      )}

      {similarImages.length > 0 && (
        <div>
          <h2>Imágenes Más Cercanas:</h2>
          <div className="image-container">
            {similarImages.map((img, index) => (
              <img key={index} src={`data:image/png;base64,${img}`} alt={`Imagen Encontrada ${index}`} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default HomePage;
