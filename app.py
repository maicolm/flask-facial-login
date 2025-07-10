# ----------------------------------------------
# app.py: Archivo principal de la aplicación Flask
# ----------------------------------------------
import os  # <--- Importación añadida para leer variables de entorno
from flask import Flask
from flask_cors import CORS

from routes.auth_routes import auth_bp         # Blueprint para autenticación (login, logout)
from routes.registro_routes import registro_bp # Blueprint para registro facial
from routes.usuario_routes import usuario_bp   # CRUD de usuarios
from routes.api_routes import api_bp           # API login facial
from routes.reinicio_routes import reinicio_bp

# ----------------------------------------------
# Inicializamos la aplicación Flask
# ----------------------------------------------
app = Flask(__name__)

# Activar CORS para todos los orígenes y métodos
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.secret_key = 'mi_clave_secreta'  # Clave para manejar sesiones seguras

# ----------------------------------------------
# Registramos los blueprints (rutas modulares)
# ----------------------------------------------
app.register_blueprint(auth_bp)
app.register_blueprint(registro_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(api_bp)
app.register_blueprint(reinicio_bp)

# ----------------------------------------------
# Ruta de salud para verificar si Render está activo
# ----------------------------------------------
@app.route('/')
def health_check():
    return {'status': 'ok', 'message': 'API Flask activa'}

# ----------------------------------------------
# Ejecutamos la app en modo debug solo si se ejecuta directamente
# ----------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
