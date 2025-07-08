# utils/face_processing.py

import os
import cv2
import numpy as np
import base64
from joblib import load

# ----------------------------------------------
# Configuraciones globales de rutas
# ----------------------------------------------
DATASET_PATH = 'dataset'
MODELO_PATH = 'modelos/modelo_lbph.yml'
MODELO_LOGISTICO_PATH = 'modelos/modelo_logistico.pkl'

# Aseguramos que existan los directorios necesarios
os.makedirs(DATASET_PATH, exist_ok=True)
os.makedirs('modelos', exist_ok=True)

# ----------------------------------------------
# Función para decodificar una imagen base64 a formato OpenCV
# ----------------------------------------------
def decode_image(data_url):
    """
    Convierte una cadena base64 en una imagen OpenCV.
    """
    header, encoded = data_url.split(',', 1)
    img_bytes = base64.b64decode(encoded)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

# ----------------------------------------------
# Función para guardar imagenes preprocesadas de entrenamiento
# ----------------------------------------------
def save_image(img, user_id, index=1):
    """
    Guarda una imagen en escala de grises y redimensionada en el dataset,
    nombrada con el ID del usuario.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (200, 200))
    cv2.imwrite(f"{DATASET_PATH}/{user_id}_{index}.jpg", resized)

# ----------------------------------------------
# Entrena el modelo LBPH con las imágenes del dataset y lo guarda
# ----------------------------------------------
def entrenar_modelo():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, labels = [], []
    for file in os.listdir(DATASET_PATH):
        if file.endswith(".jpg"):
            path = os.path.join(DATASET_PATH, file)
            label = int(file.split('_')[0])  # Usamos ID numérico como etiqueta
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            faces.append(cv2.resize(img, (200, 200)))
            labels.append(label)
    if faces:
        recognizer.train(faces, np.array(labels))
        recognizer.save(MODELO_PATH)

# ----------------------------------------------
# Carga el modelo facial LBPH si existe
# ----------------------------------------------
def cargar_modelo():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if os.path.exists(MODELO_PATH):
        recognizer.read(MODELO_PATH)
        return recognizer
    return None

# ----------------------------------------------
# Carga el modelo de regresión logística si existe
# ----------------------------------------------
def cargar_modelo_logistico():
    if os.path.exists(MODELO_LOGISTICO_PATH):
        return load(MODELO_LOGISTICO_PATH)
    return None
