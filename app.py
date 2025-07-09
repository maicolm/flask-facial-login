# ----------------------------------------------
# app.py: Archivo principal de la aplicación Flask
# ----------------------------------------------
from flask_cors import CORS
from flask import Flask
from routes.auth_routes import auth_bp         # Blueprint para autenticación (login, logout)
from routes.registro_routes import registro_bp # Blueprint para registro facial
from routes.usuario_routes import usuario_bp   # CRUD de usuarios
from routes.api_routes import api_bp           # API login facial

# ----------------------------------------------
# Inicializamos la aplicación Flask
# ----------------------------------------------
app = Flask(__name__)
#CORS(app, resources={r"/api/*": {"origins": "*"}})  # Solo permite CORS en rutas /api/*
# Permitir cualquier origen para cualquier ruta
#CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
#CORS(app, resources={r"/api/*": {"origins": ["https://www.grupoexpertos.com"]}}, supports_credentials=True)
CORS(app, origins="*", allow_headers="*", methods=["GET", "POST", "OPTIONS"])

app.secret_key = 'mi_clave_secreta'  # Clave para manejar sesiones seguras

# ----------------------------------------------
# Registramos los blueprints (rutas modulares)
# ----------------------------------------------
app.register_blueprint(auth_bp)
app.register_blueprint(registro_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(api_bp)

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
