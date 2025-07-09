# ----------------------------------------------
# utils/database.py: Módulo para conexión con MySQL usando variables de entorno
# ----------------------------------------------

import os
import mysql.connector
from mysql.connector import Error

# ----------------------------------------------
# Establecer conexión a la base de datos
# ----------------------------------------------
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_NAME'),
            port=os.environ.get('DB_PORT', 3306)  # Railway puede usar otro puerto
        )
        if connection.is_connected():
            return connection
        else:
            print("❌ Error: conexión no establecida")
            return None
    except Error as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        return None

# ----------------------------------------------
# Función para obtener el rol de un usuario por ID
# ----------------------------------------------
def obtener_rol_usuario(id_usuario):
    try:
        connection = get_db_connection()
        if connection is None:
            return None
        cursor = connection.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener el rol del usuario: {e}")
        return None
