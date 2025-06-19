import requests
import json
from services.openai_agent import OpenAIAgent
from services.tools import ToolManager

# Configuración de la API
BASE_URL = "http://localhost:5000/api"

def test_database_connection():
    """Probar conexión a base de datos"""
    try:
        from ddbb.conection import get_conn
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cur.close()
        conn.close()
        print("✅ Conexión a base de datos: OK")
        return True
    except Exception as e:
        print(f"❌ Error conexión base de datos: {e}")
        return False

def crear_datos_prueba():
    """Crear datos de prueba usando la API"""
    usuarios_prueba = [
        {
            "nombre": "Juan Pérez",
            "email": "pyperan@gmail.com",
            "password": "password123"
        },
        {
            "nombre": "María García",
            "email": "andrescaballero@gmail.com", 
            "password": "password456"
        },
        {
            "nombre": "Carlos López",
            "email": "pypera.n@gmail.com",
            "password": "password789"
        }
    ]
    
    print("\n🔧 Creando datos de prueba...")
    
    for usuario in usuarios_prueba:
        try:
            response = requests.post(f"{BASE_URL}/usuarios", json=usuario)
            if response.status_code == 201:
                print(f"✅ Usuario creado: {usuario['nombre']}")
            else:
                print(f"⚠️ Error creando {usuario['nombre']}: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_api_endpoints():
    """Probar todos los endpoints de la API"""
    print("\n🧪 Probando endpoints de la API...")
    
    # GET - Listar usuarios
    try:
        response = requests.get(f"{BASE_URL}/usuarios")
        if response.status_code == 200:
            usuarios = response.json()
            print(f"✅ GET /usuarios: {len(usuarios)} usuarios encontrados")
        else:
            print(f"❌ GET /usuarios falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error GET usuarios: {e}")
    
    # GET - Obtener usuario por ID
    try:
        response = requests.get(f"{BASE_URL}/usuarios/1")
        if response.status_code == 200:
            usuario = response.json()
            print(f"✅ GET /usuarios/1: {usuario.get('nombre', 'Usuario encontrado')}")
        else:
            print(f"⚠️ GET /usuarios/1: {response.status_code}")
    except Exception as e:
        print(f"❌ Error GET usuario por ID: {e}")
    
    # PUT - Actualizar usuario
    try:
        update_data = {"nombre": "Juan Pérez Actualizado"}
        response = requests.put(f"{BASE_URL}/usuarios/1", json=update_data)
        if response.status_code == 200:
            print("✅ PUT /usuarios/1: Usuario actualizado")
        else:
            print(f"⚠️ PUT /usuarios/1: {response.status_code}")
    except Exception as e:
        print(f"❌ Error PUT usuario: {e}")

def test_openai_agent():
    """Probar el agente de OpenAI"""
    print("\n🤖 Probando agente de OpenAI...")
    
    try:
        agent = OpenAIAgent()
        
        # Probar diferentes tipos de mensajes
        mensajes_prueba = [
            "Hola, ¿cómo estás?",
            "Envía un correo a juan@test.com",
            "Quiero crear un nuevo usuario",
            "Muéstrame todos los usuarios",
            "Adiós"
        ]
        
        for mensaje in mensajes_prueba:
            print(f"\n📨 Usuario: {mensaje}")
            resultado = agent.procesar_mensaje(mensaje)
            print(f"🎯 Intención: {resultado['intencion']}")
            print(f"📝 Entidades: {resultado['entidades']}")
            print(f"🤖 Respuesta: {resultado['respuesta']}")
            
    except Exception as e:
        print(f"❌ Error probando agente OpenAI: {e}")
        print("💡 Asegúrate de tener OPENAI_API_KEY configurado en el .env")

def test_tools():
    """Probar las herramientas"""
    print("\n🛠️ Probando herramientas...")
    
    try:
        tools = ToolManager()
        
        # Probar generación de password
        password = tools.generar_password_temporal()
        print(f"✅ Password temporal generado: {password}")
        
        # Probar validación de email
        email_valido = tools.validar_email("test@example.com")
        email_invalido = tools.validar_email("email-malo")
        print(f"✅ Validación email válido: {email_valido}")
        print(f"✅ Validación email inválido: {email_invalido}")
        
        # Probar estadísticas
        stats = tools.obtener_estadisticas_usuarios()
        print(f"✅ Estadísticas usuarios: {stats}")
        
        # Probar envío de email (solo si está configurado)
        if hasattr(tools, 'resend') and tools.resend:
            print("📧 Probando envío de email...")
            resultado = tools.enviar_email_saludo("test@example.com", "Usuario de Prueba")
            print(f"📧 Resultado envío: {resultado}")
        else:
            print("⚠️ Resend no configurado. Agrega RESEND_API_KEY al .env para probar emails")
            
    except Exception as e:
        print(f"❌ Error probando herramientas: {e}")

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA")
    print("=" * 50)
    
    # 1. Probar conexión a base de datos
    if not test_database_connection():
        print("❌ No se puede continuar sin conexión a base de datos")
        return
    
    # 2. Crear datos de prueba
    crear_datos_prueba()
    
    # 3. Probar API endpoints
    test_api_endpoints()
    
    # 4. Probar agente OpenAI
    test_openai_agent()
    
    # 5. Probar herramientas
    test_tools()
    
    print("\n" + "=" * 50)
    print("🎉 PRUEBAS COMPLETADAS")

if __name__ == "__main__":
    main()