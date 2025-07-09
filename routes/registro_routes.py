from flask import Blueprint, request, jsonify
from utils.face_processing import decode_image, save_image
from utils.model_utils import entrenar_modelo
from utils.database import get_db_connection
import os

registro_bp = Blueprint('registro_bp', __name__)

@registro_bp.route('/api/registro', methods=['POST'])
def registro():
    data = request.get_json()
    username = data.get('username')
    fotos = data.get('fotos', [])

    if not username or not fotos:
        return jsonify({'success': False, 'message': 'Datos incompletos'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, nivel) VALUES (%s, %s)", (username, 'operador'))
        conn.commit()
        user_id = cursor.lastrowid
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    for i, foto_b64 in enumerate(fotos):
        img = decode_image(foto_b64)
        save_image(img, user_id, i + 1)

    # ⚠️ Entrenar modelo cada vez que se registra un nuevo usuario
    entrenar_modelo()

    return jsonify({'success': True, 'message': 'Usuario registrado y modelo entrenado'})
