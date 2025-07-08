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
