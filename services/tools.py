import resend
import os
from dotenv import load_dotenv
from config.settings import Config
import logging

# Cargar variables de entorno al importar
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ToolManager:
    """
    Gestor de herramientas para el agente de IA
    """
    
    def __init__(self):
        # Cargar variables de entorno por si acaso
        load_dotenv()
        
        # Configurar Resend
        api_key = Config.RESEND_API_KEY or os.getenv('RESEND_API_KEY')
        if api_key:
            resend.api_key = api_key
            print(f"✅ Resend configurado: {api_key[:8]}...{api_key[-4:]}")
        else:
            print("⚠️ RESEND_API_KEY no configurado")
            
        self.from_email = Config.FROM_EMAIL or os.getenv('FROM_EMAIL', 'onboarding@resend.dev')
    
    def enviar_email_saludo(self, destinatario, nombre_destinatario=None):
        """
        Herramienta para enviar un email de saludo como ejemplo/testing usando Resend
        
        Args:
            destinatario (str): Email del destinatario
            nombre_destinatario (str, optional): Nombre del destinatario
            
        Returns:
            str: Mensaje de confirmación o error
        """
        try:
            # Validar configuración de Resend
            if not resend.api_key:
                return "❌ Error: Resend no configurado. Verifica RESEND_API_KEY en las variables de entorno."
            
            # Verificar si es un email de testing válido
            emails_testing_validos = [
                'delivered@resend.dev',
                'bounced@resend.dev', 
                'complained@resend.dev'
            ]
            
            # Si es un email de prueba (test.com, example.com, etc), usar email de testing
            dominios_invalidos = ['test.com', 'example.com', 'testing.com', 'demo.com']
            email_final = destinatario
            
            if any(dominio in destinatario.lower() for dominio in dominios_invalidos):
                email_final = 'delivered@resend.dev'
                mensaje_testing = f" (Email redirigido de {destinatario} a email de testing válido)"
            else:
                mensaje_testing = ""
            
            # Preparar el contenido del email
            nombre = nombre_destinatario if nombre_destinatario else "amigo/a"
            
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #333;">¡Hola {nombre}! 👋</h2>
                
                <p>Este es un email de saludo enviado automáticamente desde tu API de gestión de usuarios.</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>🤖 Funcionalidad de testing</strong></p>
                    <p>Este email se envió como prueba de la funcionalidad de herramientas del agente de IA.</p>
                    {f'<p><strong>📧 Email original:</strong> {destinatario}</p>' if mensaje_testing else ''}
                </div>
                
                <p>¡Saludos!</p>
                <p><strong>Tu Sistema de Gestión de Usuarios</strong></p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 12px;">Este es un email automático de testing enviado con Resend.</p>
            </div>
            """
            
            text_content = f"""
            ¡Hola {nombre}!
            
            Este es un email de saludo enviado automáticamente desde tu API de gestión de usuarios.
            
            Este email se envió como prueba de la funcionalidad de herramientas del agente de IA.
            
            {f'Email original: {destinatario}' if mensaje_testing else ''}
            
            ¡Saludos!
            Tu Sistema de Gestión de Usuarios
            
            ---
            Este es un email automático de testing enviado con Resend.
            """
            
            # Enviar el email usando Resend
            params = {
                "from": self.from_email,
                "to": [email_final],
                "subject": "¡Saludo desde tu API! 🚀",
                "html": html_content,
                "text": text_content,
            }
            
            response = resend.Emails.send(params)
            
            if response and response.get('id'):
                logger.info(f"Email de saludo enviado exitosamente a {email_final}. ID: {response.get('id')}")
                return f"✅ Email de saludo enviado exitosamente a {destinatario}{mensaje_testing}"
            else:
                logger.error(f"Respuesta inesperada de Resend: {response}")
                return f"❌ Error: Respuesta inesperada de Resend"
            
        except Exception as e:
            error_msg = str(e)
            
            # Manejo específico para errores de validación de Resend
            if "validation_error" in error_msg or "Invalid `to` field" in error_msg:
                return f"⚠️ Email no enviado: Resend en modo testing solo acepta emails verificados. Prueba con: delivered@resend.dev"
            elif "test.com" in error_msg:
                return f"⚠️ Email no enviado: Dominio {destinatario.split('@')[1]} no permitido en modo testing. Usa delivered@resend.dev"
            else:
                logger.error(f"Error enviando email con Resend: {error_msg}")
                return f"❌ Error enviando email: {error_msg}"
    
    def enviar_email_personalizado(self, destinatario, asunto, mensaje, nombre_destinatario=None):
        """
        Herramienta para enviar emails personalizados usando Resend
        
        Args:
            destinatario (str): Email del destinatario
            asunto (str): Asunto del email
            mensaje (str): Cuerpo del mensaje
            nombre_destinatario (str, optional): Nombre del destinatario
            
        Returns:
            str: Mensaje de confirmación o error
        """
        try:
            if not resend.api_key:
                return "Error: Configuración de Resend incompleta. Verifica RESEND_API_KEY."
            
            # Personalizar mensaje si se proporciona nombre
            saludo = f"Hola {nombre_destinatario}," if nombre_destinatario else "Hola,"
            
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <p>{saludo}</p>
                
                <div style="margin: 20px 0;">
                    {mensaje.replace('\n', '<br>')}
                </div>
                
                <p>Saludos,<br>
                <strong>Tu Sistema de Gestión de Usuarios</strong></p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 12px;">Email enviado automáticamente con Resend.</p>
            </div>
            """
            
            text_content = f"{saludo}\n\n{mensaje}\n\nSaludos,\nTu Sistema de Gestión de Usuarios"
            
            # Enviar el email
            params = {
                "from": self.from_email,
                "to": [destinatario],
                "subject": asunto,
                "html": html_content,
                "text": text_content,
            }
            
            response = resend.Emails.send(params)
            
            logger.info(f"Email personalizado enviado a {destinatario}. ID: {response.get('id')}")
            return f"✅ Email enviado exitosamente a {destinatario}"
            
        except Exception as e:
            error_msg = f"Error enviando email personalizado con Resend: {str(e)}"
            logger.error(error_msg)
            return f"❌ {error_msg}"
    
    def enviar_email_bienvenida(self, destinatario, nombre_usuario, password_temporal=None):
        """
        Herramienta para enviar email de bienvenida a nuevos usuarios
        
        Args:
            destinatario (str): Email del destinatario
            nombre_usuario (str): Nombre del usuario
            password_temporal (str, optional): Password temporal si aplica
            
        Returns:
            str: Mensaje de confirmación o error
        """
        try:
            if not resend.api_key:
                return "Error: Configuración de Resend incompleta."
            
            password_info = ""
            if password_temporal:
                password_info = f"""
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107;">
                    <h4 style="margin: 0 0 10px 0; color: #856404;">🔐 Credenciales temporales:</h4>
                    <p style="margin: 0;"><strong>Password temporal:</strong> <code style="background: #f8f9fa; padding: 4px 8px; border-radius: 4px;">{password_temporal}</code></p>
                    <p style="margin: 10px 0 0 0; font-size: 14px; color: #856404;">Por favor, cambia tu contraseña después del primer inicio de sesión.</p>
                </div>
                """
            
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #28a745;">¡Bienvenido/a {nombre_usuario}! 🎉</h2>
                
                <p>Tu cuenta ha sido creada exitosamente en nuestro sistema de gestión de usuarios.</p>
                
                {password_info}
                
                <div style="background-color: #e7f3ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="margin: 0 0 10px 0;">📋 Próximos pasos:</h4>
                    <ul style="margin: 0; padding-left: 20px;">
                        <li>Completa tu perfil</li>
                        <li>Explora las funcionalidades disponibles</li>
                        <li>Contacta soporte si necesitas ayuda</li>
                    </ul>
                </div>
                
                <p>Si tienes alguna pregunta, no dudes en contactarnos.</p>
                
                <p>¡Gracias por unirte a nosotros!<br>
                <strong>El equipo de desarrollo</strong></p>
            </div>
            """
            
            params = {
                "from": self.from_email,
                "to": [destinatario],
                "subject": f"¡Bienvenido/a {nombre_usuario}! Tu cuenta está lista 🚀",
                "html": html_content,
            }
            
            response = resend.Emails.send(params)
            
            logger.info(f"Email de bienvenida enviado a {destinatario}. ID: {response.get('id')}")
            return f"✅ Email de bienvenida enviado a {nombre_usuario}"
            
        except Exception as e:
            error_msg = f"Error enviando email de bienvenida: {str(e)}"
            logger.error(error_msg)
            return f"❌ {error_msg}"
    
    def validar_email(self, email):
        """
        Herramienta para validar formato de email
        
        Args:
            email (str): Email a validar
            
        Returns:
            bool: True si el email es válido, False si no
        """
        import re
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def generar_password_temporal(self, longitud=8):
        """
        Herramienta para generar passwords temporales
        
        Args:
            longitud (int): Longitud del password a generar
            
        Returns:
            str: Password temporal generado
        """
        import random
        import string
        
        # Asegurar que tenga al menos una mayúscula, minúscula, número y símbolo
        mayusculas = string.ascii_uppercase
        minusculas = string.ascii_lowercase
        numeros = string.digits
        simbolos = "!@#$%&*"
        
        # Generar password con al menos un carácter de cada tipo
        password = [
            random.choice(mayusculas),
            random.choice(minusculas),
            random.choice(numeros),
            random.choice(simbolos)
        ]
        
        # Completar la longitud restante
        todos_caracteres = mayusculas + minusculas + numeros + simbolos
        for _ in range(longitud - 4):
            password.append(random.choice(todos_caracteres))
        
        # Mezclar la lista y convertir a string
        random.shuffle(password)
        password_final = ''.join(password)
        
        logger.info("Password temporal generado")
        return password_final
    
    def obtener_estadisticas_usuarios(self):
        """
        Herramienta para obtener estadísticas básicas de usuarios
        
        Returns:
            dict: Estadísticas de usuarios
        """
        try:
            from models.usuario import Usuario
            usuarios = Usuario.obtener_todos()
            
            estadisticas = {
                "total_usuarios": len(usuarios),
                "usuarios_con_gmail": len([u for u in usuarios if 'gmail.com' in u.get('email', '')]),
                "dominios_email": list(set([u.get('email', '').split('@')[-1] for u in usuarios if '@' in u.get('email', '')])),
                "usuarios_recientes": len([u for u in usuarios if u.get('fecha_creacion')]),
            }
            
            return estadisticas
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {"error": str(e)}