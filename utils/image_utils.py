# ----------------------------------------------
# utils/image_utils.py: Funciones para trabajar con imágenes base64
# ----------------------------------------------
import base64
import numpy as np
import cv2

# ----------------------------------------------
# Función para decodificar imagen base64 enviada desde el frontend
# ----------------------------------------------
def decode_image(data_url):
    """
    Convierte una imagen codificada en base64 (tipo data URL) a una imagen OpenCV (numpy array).
    - data_url: cadena que comienza con "data:image/jpeg;base64,..."
    - Retorna: imagen en formato OpenCV BGR (3 canales)
    """
    try:
        header, encoded = data_url.split(',', 1)  # Separa el encabezado del contenido base64
        img_bytes = base64.b64decode(encoded)      # Decodifica la cadena base64 a bytes
        np_arr = np.frombuffer(img_bytes, np.uint8)  # Crea un array numpy con los bytes
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # Decodifica a imagen OpenCV en color
        return img
    except Exception as e:
        print(f"Error al decodificar imagen: {e}")
        return None
