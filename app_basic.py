from flask import Flask
from dotenv import load_dotenv
from config.settings import Config
from routes.usuario_routes import usuario_bp
from models.usuario import crear_tabla

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Registrar solo blueprint de usuarios (sin chat)
    app.register_blueprint(usuario_bp, url_prefix='/api')
    
    # Crear tablas si no existen
    crear_tabla()
    
    @app.route('/')
    def home():
        return {
            "message": "API de Gestión de Usuarios - Versión Básica",
            "endpoints": {
                "usuarios": {
                    "GET /api/usuarios": "Listar usuarios",
                    "POST /api/usuarios": "Crear usuario",
                    "GET /api/usuarios/{id}": "Obtener usuario",
                    "PUT /api/usuarios/{id}": "Actualizar usuario", 
                    "DELETE /api/usuarios/{id}": "Eliminar usuario"
                }
            }
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0")