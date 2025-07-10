# utils/face_processing.py

import os
import cv2
import numpy as np
import base64
from joblib import load
from sklearn.linear_model import LogisticRegression
import joblib
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


# ----------------------------------------------
# Función para detectar rostro, convertir a gris, recortar y redimensionar
# ----------------------------------------------
def detectar_y_preprocesar(img, size=(100, 100)):
    """
    Detecta un rostro en la imagen, lo convierte a escala de grises,
    lo recorta y lo redimensiona al tamaño dado.
    Retorna un vector listo para el modelo (flattened).
    """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        return None  # No se detectó rostro

    x, y, w, h = faces[0]
    rostro = gray[y:y+h, x:x+w]
    rostro_redimensionado = cv2.resize(rostro, size)
    return rostro_redimensionado.flatten().reshape(1, -1)


# ----------------------------------------------
# Entrenamiento del modelo de regresión logística
# ----------------------------------------------
def entrenar_modelo_logistico():
    X, y = [], []
    for file in os.listdir(DATASET_PATH):
        if file.endswith(".jpg"):
            path = os.path.join(DATASET_PATH, file)
            label = int(file.split('_')[0])
            img = cv2.imread(path)
            features = detectar_y_preprocesar(img)
            if features is not None:
                X.append(features[0])
                y.append(label)

    if not X:
        mensaje = "⚠️ No se encontraron datos válidos para entrenar el modelo logístico."
        print(mensaje)
        return mensaje

    if len(set(y)) < 2:
        mensaje = "⚠️ No se entrenó el modelo logístico: se necesita al menos 2 usuarios diferentes."
        print(mensaje)
        return mensaje

    model = LogisticRegression(max_iter=1000)
    model.fit(np.array(X), np.array(y))
    joblib.dump(model, MODELO_LOGISTICO_PATH)
    print("✅ Modelo de regresión logística entrenado y guardado.")
    return None
