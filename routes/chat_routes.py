from flask import Blueprint, request, jsonify
from services.openai_agent import OpenAIAgent

# Crear blueprint para las rutas de chat
chat_bp = Blueprint('chat', __name__)

# Variable global para el agente (se inicializará cuando se necesite)
agent = None

def get_agent():
    """Obtener instancia del agente (inicialización lazy)"""
    global agent
    if agent is None:
        agent = OpenAIAgent()
    return agent

@chat_bp.route('/chat', methods=['POST'])
def procesar_mensaje():
    """
    Procesar mensaje del usuario con el agente de IA
    
    Ejemplo de request:
    {
        "mensaje": "Hola, envía un correo a juan@test.com"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'mensaje' not in data:
            return jsonify({'error': 'Se requiere el campo "mensaje"'}), 400
        
        mensaje_usuario = data['mensaje']
        
        # Procesar mensaje con el agente de IA
        current_agent = get_agent()
        resultado = current_agent.procesar_mensaje(mensaje_usuario)
        
        return jsonify({
            'success': True,
            'mensaje_usuario': mensaje_usuario,
            'intencion': resultado['intencion'],
            'entidades': resultado['entidades'],
            'respuesta': resultado['respuesta']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chat_bp.route('/chat/intenciones', methods=['GET'])
def listar_intenciones():
    """
    Listar todas las intenciones disponibles del agente
    """
    current_agent = get_agent()
    return jsonify({
        'intenciones': current_agent.intenciones
    }), 200

@chat_bp.route('/chat/health', methods=['GET'])
def health_check():
    """
    Verificar el estado del agente de IA
    """
    try:
        # Probar conexión con OpenAI
        current_agent = get_agent()
        test_response = current_agent.detectar_intencion("test")
        
        return jsonify({
            'status': 'ok',
            'openai_connected': True,
            'message': 'Agente de IA funcionando correctamente'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'openai_connected': False,
            'error': str(e)
        }), 500