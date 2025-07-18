# ----------------------------------------------
# registro_routes.py: Módulo de rutas para el registro facial
# ----------------------------------------------

from flask import Blueprint, request, jsonify
import cv2
from utils.database import get_db_connection
from utils.face_processing import decode_image, save_image, entrenar_modelo, cargar_modelo
from utils.face_processing import entrenar_modelo_logistico  # <- ya importado

# Definimos correctamente el blueprint
registro_bp = Blueprint('registro_bp', __name__)

@registro_bp.route('/api/registro', methods=['POST', 'OPTIONS'])
def registro():
    # Respuesta CORS preflight
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    username = data.get('username')
    fotos = data.get('fotos', [])

    if not username or not fotos:
        return jsonify({'success': False, 'message': 'Datos incompletos'}), 400

    # Verificamos si el nombre de usuario ya existe
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'El usuario ya existe'}), 409
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error en la base de datos: {str(e)}'}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    # Verificamos si el rostro ya fue registrado
    modelo = cargar_modelo()
    if modelo:
        img = decode_image(fotos[0])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (200, 200))
        pred_label, confidence = modelo.predict(resized)
        if confidence < 50:
            return jsonify({'success': False, 'message': 'Este rostro ya está registrado'}), 409

    # Insertamos nuevo usuario
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, nivel) VALUES (%s, %s)", (username, 'administrador'))
        conn.commit()
        user_id = cursor.lastrowid
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al registrar usuario: {str(e)}'}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    # Guardamos las imágenes
    for i, foto_b64 in enumerate(fotos):
        img = decode_image(foto_b64)
        save_image(img, user_id, i + 1)

    # Entrenamiento de modelos
    entrenar_modelo()
    advertencia_logistico = entrenar_modelo_logistico()

    return jsonify({
        'success': True,
        'message': 'Usuario registrado exitosamente.',
        'advertencia': advertencia_logistico or ''
    })
