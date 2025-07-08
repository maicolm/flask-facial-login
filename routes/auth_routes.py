# ----------------------------------------------
# auth_routes.py: Rutas relacionadas con login y autenticación facial
# ----------------------------------------------

from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
import cv2
import numpy as np

from utils.database import get_db_connection

from utils.face_processing import decode_image
from utils.modelo import cargar_modelo, cargar_modelo_logistico

# ----------------------------------------------
# Definimos el blueprint de autenticación
# ----------------------------------------------
auth_bp = Blueprint('auth_bp', __name__)

# ----------------------------------------------
# Ruta: /login
# Descripción: Inicia sesión mediante reconocimiento facial
# ----------------------------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    face_data = request.form['face_data']

    # Validación de campos enviados
    if not username or not face_data:
        return jsonify({'success': False, 'message': 'Datos incompletos'}), 400

    # Decodificamos la imagen en formato base64 enviada desde el frontend
    img = decode_image(face_data)

    # Cargamos los modelos LBPH (reconocimiento) y logístico (probabilidad)
    modelo = cargar_modelo()
    modelo_logistico = cargar_modelo_logistico()

    if modelo is None or modelo_logistico is None:
        return jsonify({'success': False, 'message': 'Modelos no entrenados'}), 500

    # Convertimos imagen a escala de grises y la redimensionamos
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (200, 200))

    # ----------------------------------------------
    # Obtenemos el ID real del usuario desde la base de datos
    # Este ID fue usado como etiqueta (label) al entrenar el modelo
    # ----------------------------------------------
    label = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            label = result[0]  # ID del usuario
        else:
            return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    # ----------------------------------------------
    # Realizamos predicción con el modelo facial (LBPH)
    # ----------------------------------------------
    pred_label, confidence = modelo.predict(resized)

    # Evaluamos probabilidad con el modelo logístico
    probabilidad = modelo_logistico.predict_proba([[confidence]])[0][1]

    # Mostramos info útil en consola para depuración
    print("USERNAME:", username)
    print("Etiqueta esperada:", label)
    print("Etiqueta predicha:", pred_label)
    print("Confianza:", confidence)
    print("Probabilidad (modelo logístico):", probabilidad)

    # ----------------------------------------------
    # Validamos que coincida la etiqueta y que la probabilidad sea ≥ 80%
    # ----------------------------------------------
    if pred_label == label and probabilidad >= 0.80:
        # Guardamos datos de sesión para uso posterior
        session['usuario'] = username

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT nivel FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            if result:
                session['nivel'] = result[0]  # Puede ser 'administrador' o 'operador'
        except:
            session['nivel'] = 'operador'  # Valor por defecto si ocurre error
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

        return jsonify({'success': True})
    else:
        return jsonify({
            'success': False,
            'message': f'Rostro no coincide o probabilidad muy baja ({round(probabilidad*100)}%)'
        })

# ----------------------------------------------
# Ruta protegida: /bienvenido
# Descripción: Muestra dashboard según nivel de usuario
# ----------------------------------------------
@auth_bp.route('/bienvenido')
def bienvenido():
    if 'usuario' in session:
        return render_template(
            'dashboard.html',
            usuario=session['usuario'],
            nivel=session.get('nivel', 'operador')
        )
    return redirect(url_for('index'))

# ----------------------------------------------
# Ruta: /logout
# Descripción: Cierra la sesión del usuario
# ----------------------------------------------
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
