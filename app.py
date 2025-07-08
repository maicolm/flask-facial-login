# ----------------------------------------------
# app.py: Archivo principal de la aplicación Flask
# ----------------------------------------------
from flask_cors import CORS
from flask import Flask
from routes.auth_routes import auth_bp         # Blueprint para autenticación (login, logout)
from routes.registro_routes import registro_bp # Blueprint para registro facial
from routes.usuario_routes import usuario_bp   # ✅ NUEVO: Blueprint para CRUD de usuarios


# ----------------------------------------------
# Inicializamos la aplicación Flask
# ----------------------------------------------
app = Flask(__name__)
#CORS(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key = 'mi_clave_secreta'  # Clave para manejar sesiones seguras

# ----------------------------------------------
# Registramos los blueprints (rutas modulares)
# ----------------------------------------------
app.register_blueprint(auth_bp)
app.register_blueprint(registro_bp)
app.register_blueprint(usuario_bp)  # ✅ Se registra el CRUD de usuarios


# ----------------------------------------------
# Ruta de inicio (formulario HTML principal)
# ----------------------------------------------
@app.route('/')
def index():
    from flask import render_template
    return render_template('index.html')

# ----------------------------------------------
# Ruta protegida: dashboard que se muestra después del login
# ----------------------------------------------
@app.route('/bienvenido')
def bienvenido():
    from flask import session, render_template, redirect, url_for
    if 'usuario' in session:
        return render_template('dashboard.html', usuario=session['usuario'], nivel=session.get('nivel', 'operador'))
    return redirect(url_for('index'))

# ----------------------------------------------
# Ruta para cerrar sesión
# ----------------------------------------------
@app.route('/logout')
def logout():
    from flask import session, redirect, url_for
    session.clear()
    return redirect(url_for('index'))

# ----------------------------------------------
# Ejecutamos la app en modo debug solo si se ejecuta directamente
# ----------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
