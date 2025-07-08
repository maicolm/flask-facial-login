# ----------------------------------------------
# utils/database.py: Módulo para conexión con MySQL
# ----------------------------------------------
import mysql.connector
from mysql.connector import Error

# Función para crear una conexión a la base de datos MySQL
# Se usa en los controladores para acceder a la tabla de usuarios

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',        # Servidor local
            user='root',             # Usuario por defecto
            password='',             # Contraseña (puedes cambiarla si aplica)
            database='facial_login'  # Nombre de tu base de datos
        )
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
