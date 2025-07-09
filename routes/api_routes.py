from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import base64
import os
import pickle

from utils.database import obtener_rol_usuario

api_bp = Blueprint('api_bp', __name__)

# Función para cargar los modelos entrenados
def cargar_modelos():
    try:
        with open('modelos/modelo_pca.pkl', 'rb') as f:
            pca = pickle.load(f)
        with open('modelos/modelo_logistico.pkl', 'rb') as f:
            modelo = pickle.load(f)
        return pca, modelo
    except Exception as e:
        print(f"❌ Error cargando los modelos: {e}")
        return None, None

# Ruta para login facial
@api_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data or 'imagen' not in data:
        return jsonify({'status': 'error', 'message': 'Imagen no proporcionada'}), 400

    try:
        # Decodificar la imagen base64
        imagen_b64 = data['imagen'].split(',')[-1]
        imagen_bytes = base64.b64decode(imagen_b64)
        imagen_array = np.frombuffer(imagen_bytes, np.uint8)
        img = cv2.imdecode(imagen_array, cv2.IMREAD_GRAYSCALE)

        if img is None:
            return jsonify({'status': 'error', 'message': 'Error al procesar la imagen'}), 400

        # Preprocesar imagen (redimensionar y aplanar)
        resized = cv2.resize(img, (100, 100)).flatten().reshape(1, -1)

        # Cargar modelos entrenados
        pca, modelo = cargar_modelos()
        if pca is None or modelo is None:
            return jsonify({'status': 'error', 'message': 'Modelos no disponibles'}), 500

        # Aplicar PCA + predicción
        X_pca = pca.transform(resized)
        id_usuario = modelo.predict(X_pca)[0]

        # Verificar el rol desde la base de datos
        rol = obtener_rol_usuario(id_usuario)
        if rol is None:
            return jsonify({'status': 'fail', 'message': 'Usuario no encontrado'}), 404

        return jsonify({
            'status': 'success',
            'id_usuario': id_usuario,
            'rol': rol
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
