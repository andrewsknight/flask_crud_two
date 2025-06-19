from flask import Blueprint
from controllers.usuario_controller import UsuarioController

# Crear blueprint para las rutas de usuario
usuario_bp = Blueprint('usuarios', __name__)

# Definir las rutas
@usuario_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    """Crear un nuevo usuario"""
    return UsuarioController.crear_usuario()

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    """Obtener todos los usuarios"""
    return UsuarioController.listar_usuarios()

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    """Obtener usuario por ID"""
    return UsuarioController.obtener_usuario(usuario_id)

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
    """Actualizar usuario"""
    return UsuarioController.actualizar_usuario(usuario_id)

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    """Eliminar usuario"""
    return UsuarioController.eliminar_usuario(usuario_id)