from flask import Blueprint, render_template, request, jsonify
from utils.database import get_db_connection

usuario_bp = Blueprint('usuario_bp', __name__)

# Vista principal del CRUD
@usuario_bp.route('/usuarios')
def vista_usuarios():
    return render_template('usuarios.html')

# API: Listar todos los usuarios
@usuario_bp.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, nivel, fc FROM users")
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# API: Actualizar nivel del usuario
@usuario_bp.route('/api/usuarios/<int:id>', methods=['PUT'])
def actualizar_nivel_usuario(id):
    datos = request.get_json()
    nuevo_nivel = datos.get('nivel')

    if nuevo_nivel not in ['operador', 'administrador']:
        return jsonify({'success': False, 'message': 'Nivel no válido'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET nivel = %s WHERE id = %s", (nuevo_nivel, id))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# API: Eliminar usuario
@usuario_bp.route('/api/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
