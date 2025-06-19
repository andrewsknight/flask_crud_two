import openai
import json
import os
import re
from dotenv import load_dotenv
from config.settings import Config
from services.tools import ToolManager

# Cargar variables de entorno al importar el módulo
load_dotenv()

class OpenAIAgent:
    def __init__(self):
        self.tool_manager = ToolManager()
        self.client = None
        
        # Intentar inicializar OpenAI
        try:
            # Cargar variables de entorno por si acaso
            load_dotenv()
            
            # Intentar obtener API key de múltiples fuentes
            api_key = (
                Config.OPENAI_API_KEY or 
                os.getenv('OPENAI_API_KEY') or
                os.environ.get('OPENAI_API_KEY')
            )
            
            if api_key and api_key.startswith('sk-'):
                self.client = openai.OpenAI(api_key=api_key)
                print("✅ OpenAI inicializado correctamente")
                print(f"🔑 API Key: {api_key[:8]}...{api_key[-4:]}")  # Mostrar solo parte de la key
            else:
                print("⚠️ OPENAI_API_KEY no encontrado o inválido")
                print(f"🔍 Valor encontrado: {api_key}")
                print("💡 Asegúrate de que empiece con 'sk-'")
        except Exception as e:
            print(f"⚠️ Error inicializando OpenAI: {e}")
            print("💡 El agente funcionará en modo básico sin IA")
        
        # Definir las intenciones disponibles
        self.intenciones = {
            "saludo": "El usuario está saludando o siendo cortés",
            "crear_usuario": "El usuario quiere crear un nuevo usuario",
            "listar_usuarios": "El usuario quiere ver todos los usuarios",
            "buscar_usuario": "El usuario quiere buscar un usuario específico",
            "actualizar_usuario": "El usuario quiere actualizar información de un usuario",
            "eliminar_usuario": "El usuario quiere eliminar un usuario",
            "enviar_email": "El usuario quiere enviar un correo electrónico",
            "pregunta_general": "El usuario tiene una pregunta general",
            "despedida": "El usuario se está despidiendo",
            "desconocida": "No se puede determinar la intención del usuario"
        }
    
    def detectar_intencion_basica(self, mensaje_usuario):
        """
        Fallback básico para detectar intenciones sin OpenAI
        """
        mensaje = mensaje_usuario.lower()
        
        if any(word in mensaje for word in ['hola', 'hello', 'hi', 'buenos', 'buenas']):
            return "saludo"
        elif any(word in mensaje for word in ['adiós', 'bye', 'hasta', 'chao']):
            return "despedida"
        elif any(word in mensaje for word in ['crear', 'nuevo', 'registrar']) and 'usuario' in mensaje:
            return "crear_usuario"
        elif any(word in mensaje for word in ['ver', 'mostrar', 'listar']) and 'usuario' in mensaje:
            return "listar_usuarios"
        elif 'buscar' in mensaje and 'usuario' in mensaje:
            return "buscar_usuario"
        elif any(word in mensaje for word in ['actualizar', 'modificar']) and 'usuario' in mensaje:
            return "actualizar_usuario"
        elif any(word in mensaje for word in ['eliminar', 'borrar']) and 'usuario' in mensaje:
            return "eliminar_usuario"
        elif any(word in mensaje for word in ['enviar', 'mandar']) and any(word in mensaje for word in ['correo', 'email']):
            return "enviar_email"
        elif any(word in mensaje for word in ['qué', 'cómo', 'ayuda', '?']):
            return "pregunta_general"
        else:
            return "desconocida"

    def detectar_intencion(self, mensaje_usuario):
        """
        Detecta la intención del usuario usando OpenAI (con fallback básico)
        """
        # Si OpenAI no está disponible, usar detección básica
        if not self.client:
            return self.detectar_intencion_basica(mensaje_usuario)
            
        try:
            # Prompt para detectar intención
            system_prompt = f"""Eres un asistente que detecta intenciones en mensajes de usuario.

Las intenciones disponibles son:
{json.dumps(self.intenciones, indent=2, ensure_ascii=False)}

Analiza el mensaje del usuario y devuelve SOLO el nombre de la intención más apropiada.
Si no estás seguro, devuelve "desconocida".

Ejemplos:
- "Hola" -> "saludo"
- "Quiero crear un usuario nuevo" -> "crear_usuario"
- "Muéstrame todos los usuarios" -> "listar_usuarios"
- "Envía un correo a Juan" -> "enviar_email"
- "Adiós" -> "despedida"
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": mensaje_usuario}
                ],
                max_tokens=20,
                temperature=0.1
            )
            
            intencion = response.choices[0].message.content.strip().lower()
            
            # Validar que la intención esté en nuestro diccionario
            if intencion not in self.intenciones:
                print(f"🔍 OpenAI devolvió: '{intencion}' - usando fallback básico")
                return self.detectar_intencion_basica(mensaje_usuario)
            
            print(f"🎯 OpenAI detectó intención: {intencion}")
            return intencion
            
        except Exception as e:
            print(f"❌ Error con OpenAI, usando detección básica: {e}")
            return self.detectar_intencion_basica(mensaje_usuario)
    
    def extraer_entidades_basico(self, mensaje_usuario, intencion):
        """
        Fallback básico para extraer entidades sin OpenAI
        """
        entidades = {}
        
        # Extraer email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, mensaje_usuario)
        if emails:
            entidades['destinatario'] = emails[0]
            entidades['email'] = emails[0]
        
        # Extraer números (posibles IDs)
        numero_pattern = r'\b\d+\b'
        numeros = re.findall(numero_pattern, mensaje_usuario)
        if numeros and intencion in ['buscar_usuario', 'actualizar_usuario', 'eliminar_usuario']:
            entidades['id'] = int(numeros[0])
        
        return entidades

    def extraer_entidades(self, mensaje_usuario, intencion):
        """
        Extrae entidades relevantes del mensaje según la intención
        """
        # Si OpenAI no está disponible, usar extracción básica
        if not self.client:
            return self.extraer_entidades_basico(mensaje_usuario, intencion)
            
        try:
            system_prompt = f"""Extrae las entidades relevantes del mensaje del usuario.
La intención detectada es: {intencion}

Devuelve SOLO un JSON con las entidades encontradas.

Ejemplos según intención:
- crear_usuario: {{"nombre": "Juan", "email": "juan@email.com"}}
- buscar_usuario: {{"id": 123, "nombre": "Juan", "email": "juan@email.com"}}
- enviar_email: {{"destinatario": "juan@email.com", "asunto": "Saludo"}}

Si no encuentras entidades, devuelve un JSON vacío: {{}}"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": mensaje_usuario}
                ],
                max_tokens=100,
                temperature=0.1
            )
            
            entidades_str = response.choices[0].message.content.strip()
            
            try:
                entidades = json.loads(entidades_str)
                return entidades
            except json.JSONDecodeError:
                return self.extraer_entidades_basico(mensaje_usuario, intencion)
            
        except Exception as e:
            print(f"❌ Error con OpenAI en extracción, usando básico: {e}")
            return self.extraer_entidades_basico(mensaje_usuario, intencion)
    
    def procesar_mensaje(self, mensaje_usuario):
        """
        Procesa un mensaje completo: detecta intención, extrae entidades y ejecuta acción
        """
        # Detectar intención
        intencion = self.detectar_intencion(mensaje_usuario)
        
        # Extraer entidades
        entidades = self.extraer_entidades(mensaje_usuario, intencion)
        
        # Ejecutar acción según la intención
        respuesta = self.ejecutar_accion(intencion, entidades, mensaje_usuario)
        
        return {
            "intencion": intencion,
            "entidades": entidades,
            "respuesta": respuesta
        }
    
    def ejecutar_accion(self, intencion, entidades, mensaje_original):
        """
        Ejecuta la acción correspondiente según la intención detectada
        """
        if intencion == "saludo":
            return "¡Hola! 👋 ¿En qué puedo ayudarte hoy?"
        
        elif intencion == "despedida":
            return "¡Hasta luego! 👋 Que tengas un buen día."
        
        elif intencion == "enviar_email":
            if "destinatario" in entidades:
                return self.tool_manager.enviar_email_saludo(entidades["destinatario"])
            else:
                return "Para enviar un email, necesito que me proporciones el destinatario."
        
        elif intencion == "crear_usuario":
            return "Para crear un usuario, usa el endpoint POST /api/usuarios con los datos: nombre, email y password."
        
        elif intencion == "listar_usuarios":
            return "Para ver todos los usuarios, usa el endpoint GET /api/usuarios"
        
        elif intencion == "buscar_usuario":
            return "Para buscar un usuario, usa el endpoint GET /api/usuarios/{id}"
        
        elif intencion == "actualizar_usuario":
            return "Para actualizar un usuario, usa el endpoint PUT /api/usuarios/{id}"
        
        elif intencion == "eliminar_usuario":
            return "Para eliminar un usuario, usa el endpoint DELETE /api/usuarios/{id}"
        
        elif intencion == "pregunta_general":
            return self.responder_pregunta_general(mensaje_original)
        
        else:
            return "No entiendo tu solicitud. ¿Podrías ser más específico?"
    
    def responder_pregunta_general(self, pregunta):
        """
        Responde preguntas generales usando OpenAI (con fallback básico)
        """
        # Si OpenAI no está disponible, respuesta básica
        if not self.client:
            return "Soy un asistente para la API de gestión de usuarios. Puedo ayudarte con crear, listar, buscar, actualizar y eliminar usuarios, así como enviar emails. ¿En qué puedo ayudarte específicamente?"
            
        try:
            system_prompt = """Eres un asistente útil para una API de gestión de usuarios.
Responde de manera concisa y amigable.
Si la pregunta no está relacionada con el sistema, redirige gentilmente al tema."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": pregunta}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ Error con OpenAI: {e}")
            return "Lo siento, tengo problemas para procesar tu pregunta. Soy un asistente para la API de usuarios. ¿Puedo ayudarte con algo específico sobre usuarios o emails?"