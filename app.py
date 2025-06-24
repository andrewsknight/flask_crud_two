from flask import Flask
from dotenv import load_dotenv
from config.settings import Config
from routes.usuario_routes import usuario_bp
from routes.chat_routes import chat_bp
from models.usuario import crear_tabla
from flask_cors import CORS
from flask import Flask


load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Registrar blueprints
    app.register_blueprint(usuario_bp, url_prefix='/api')
    app.register_blueprint(chat_bp, url_prefix='/api')
    
    # Crear tablas si no existen
    crear_tabla()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0")