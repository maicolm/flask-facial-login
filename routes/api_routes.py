from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import base64
from utils.modelo import reconocer_rostro_con_modelo
from utils.database import obtener_rol_usuario

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data or 'imagen' not in data:
        return jsonify({'status': 'error', 'message': 'Imagen no proporcionada'}), 400

    try:
        imagen_b64 = data['imagen'].split(',')[-1]
        imagen_bytes = base64.b64decode(imagen_b64)
        imagen_array = np.frombuffer(imagen_bytes, np.uint8)
        img = cv2.imdecode(imagen_array, cv2.IMREAD_COLOR)

        id_usuario = reconocer_rostro_con_modelo(img)
        if id_usuario is None:
            return jsonify({'status': 'fail', 'message': 'No reconocido'})

        rol = obtener_rol_usuario(id_usuario)
        return jsonify({
            'status': 'success',
            'id_usuario': id_usuario,
            'rol': rol
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
