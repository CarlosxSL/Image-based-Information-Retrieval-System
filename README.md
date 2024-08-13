# Image Based Information Retrieval System

Este proyecto es un motor de búsqueda que permite a los usuarios realizar consultas utilizando imágenes en lugar de texto. El sistema es capaz de encontrar imágenes similares dentro de una base de datos dada, aprovechando modelos de aprendizaje profundo para la extracción de características y la comparación de similitud.

## Estructura del Proyecto

El repositorio está organizado en dos carpetas principales:

- **Frontend**: Desarrollado con React y Next.js.
- **Backend**: Desarrollado con Flask.

## Características

### Extracción de Características

- **Modelo Inception**: Utilizamos el modelo preentrenado **Inception** para extraer características representativas de las imágenes. Este modelo, una red neuronal convolucional profunda, ha sido entrenado en un extenso conjunto de datos de imágenes, lo que le permite captar patrones visuales complejos que son esenciales para la comparación de similitud.

### Comparación de Similitud

- **Red Neuronal para Similitud**: Las características extraídas de las imágenes se comparan mediante una red neuronal que calcula la similitud entre ellas. Este enfoque asegura una identificación precisa y eficiente de imágenes visualmente similares dentro de la base de datos.

### Frontend

- **Interfaz de Usuario**: Permite a los usuarios subir imágenes y visualizar los resultados de la búsqueda.
- **Navegación Eficiente**: Aprovecha las capacidades de Next.js para una navegación rápida y optimizada.
- **Componentes Dinámicos**: Implementación de componentes React para una experiencia de usuario fluida e interactiva.

### Backend

- **API RESTful**: Desarrollada con Flask para manejar las solicitudes del frontend y procesar imágenes.
- **Integración con Inception**: El backend extrae características de las imágenes utilizando el modelo Inception.
- **Base de Datos MongoDB**: Almacenamiento y recuperación eficiente de imágenes en una base de datos MongoDB.
- **Comparación de Imágenes**: Uso de redes neuronales para la comparación de similitud entre las imágenes de la base de datos y la imagen consultada.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes componentes:

- **Node.js** y **npm**: Necesarios para ejecutar el frontend.
- **Python 3.x**: Necesario para ejecutar el backend.
- **MongoDB**: Base de datos para almacenar y recuperar las imágenes.

## Instalación y Uso

Sigue estos pasos para configurar y ejecutar el proyecto:

### 1. Clonar el Repositorio

```bash
git clone https://github.com/CarlosxSL/Image-based-Information-Retrieval-System.git
cd Image-based-Information-Retrieval-System
```
### 2. Cargar la Base de Datos

- Ejecuta el archivo proj02.ipynb para procesar y preparar los datos.
- Carga la base de datos MongoDB ejecutando el archivo upload_db.ipynb.
### 3. Configuración del Backend

Ve a la carpeta backend:
```bash
cd backend
```
Inicia el servidor Flask ejecutando app.py:
```bash
python app.py
 ```
### 4. Configuración del Frontend

Ve a la carpeta frontend:
```bash
cd ../frontend
```
Instala las dependencias:
```bash
npm install
```
Inicia el servidor de desarrollo:
```bash
npm run dev
```
## Uso del Sistema

- Asegúrate de que ambos servidores (backend y frontend) estén en ejecución.
- Abre tu navegador y ve a la URL: http://localhost:3000.
- Sube una imagen a través de la interfaz y observa los resultados de las imágenes similares encontradas por el sistema.
