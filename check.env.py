#!/usr/bin/env python3
"""
Script para verificar que las variables de entorno se cargan correctamente
"""

import os
from dotenv import load_dotenv

def main():
    print("🔍 VERIFICANDO VARIABLES DE ENTORNO")
    print("=" * 50)
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Variables a verificar
    variables = [
        'POSTGRES_HOST',
        'POSTGRES_PORT', 
        'POSTGRES_DB',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD',
        'OPENAI_API_KEY',
        'RESEND_API_KEY',
        'SECRET_KEY'
    ]
    
    print("📂 Contenido del archivo .env:")
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    # Ocultar valores sensibles
                    if 'KEY' in line or 'PASSWORD' in line:
                        parts = line.split('=', 1)
                        if len(parts) == 2:
                            key, value = parts
                            if value:
                                masked_value = value[:8] + '*' * (len(value) - 8) if len(value) > 8 else '*' * len(value)
                                print(f"  {i:2}: {key}={masked_value}")
                            else:
                                print(f"  {i:2}: {key}= (vacío)")
                    else:
                        print(f"  {i:2}: {line}")
    except FileNotFoundError:
        print("❌ Archivo .env no encontrado")
        return
    
    print(f"\n🔍 Variables de entorno cargadas:")
    
    for var in variables:
        value = os.getenv(var)
        if value:
            if 'KEY' in var or 'PASSWORD' in var:
                # Mostrar solo parte de las claves sensibles
                if len(value) > 8:
                    masked = value[:8] + '*' * (len(value) - 8)
                else:
                    masked = '*' * len(value)
                print(f"✅ {var} = {masked}")
            else:
                print(f"✅ {var} = {value}")
        else:
            print(f"❌ {var} = (no definida)")
    
    # Verificaciones específicas
    print(f"\n🧪 Verificaciones específicas:")
    
    # OpenAI
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        if openai_key.startswith('sk-'):
            print("✅ OPENAI_API_KEY tiene formato válido")
        else:
            print("⚠️ OPENAI_API_KEY no empieza con 'sk-'")
    else:
        print("❌ OPENAI_API_KEY no configurado")
    
    # Resend
    resend_key = os.getenv('RESEND_API_KEY') 
    if resend_key:
        if resend_key.startswith('re_'):
            print("✅ RESEND_API_KEY tiene formato válido")
        else:
            print("⚠️ RESEND_API_KEY no empieza con 're_'")
    else:
        print("❌ RESEND_API_KEY no configurado")
    
    # Base de datos
    postgres_vars = ['POSTGRES_HOST', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB']
    postgres_complete = all(os.getenv(var) for var in postgres_vars)
    if postgres_complete:
        print("✅ Variables de PostgreSQL completas")
    else:
        print("❌ Variables de PostgreSQL incompletas")
    
    print(f"\n💡 Siguiente paso:")
    if openai_key and openai_key.startswith('sk-'):
        print("  python3 app.py")
    else:
        print("  1. Configura OPENAI_API_KEY en el .env")
        print("  2. python3 app.py")

if __name__ == "__main__":
    main()