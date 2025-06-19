import os
from dotenv import load_dotenv

# Cargar variables de entorno al importar
load_dotenv()

class Config:
    """Configuración general de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tu-clave-secreta-aqui')
    
    # OpenAI
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Resend Email
    RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
    FROM_EMAIL = os.environ.get('FROM_EMAIL', 'onboarding@resend.dev')
    
    # Base de datos (si quieres centralizar la config)
    DATABASE_URL = os.environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False