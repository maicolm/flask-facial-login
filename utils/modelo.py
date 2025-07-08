import os
import joblib
import cv2
import numpy as np

MODELO_PATH = 'modelos/modelo_lbph.yml'
MODELO_LOGISTICO_PATH = 'modelos/modelo_logistico.pkl'

def cargar_modelo():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if os.path.exists(MODELO_PATH):
        recognizer.read(MODELO_PATH)
        return recognizer
    return None

def cargar_modelo_logistico():
    if os.path.exists(MODELO_LOGISTICO_PATH):
        return joblib.load(MODELO_LOGISTICO_PATH)
    return None

def reconocer_rostro_con_modelo(img):
    modelo = cargar_modelo_logistico()
    if modelo is None:
        return None

    try:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_flat = img_gray.flatten().reshape(1, -1)
        id_predicho = modelo.predict(img_flat)[0]
        return id_predicho
    except Exception as e:
        print(f"Error al reconocer el rostro: {e}")
        return None
