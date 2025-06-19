from flask import request, jsonify
from models.usuario import Usuario

class UsuarioController:
    
    @staticmethod
    def crear_usuario():
        """Crear un nuevo usuario
        
        """
        try:
            data = request.get_json()

            # Validar datos requeridos
            if not data or not all(k in data for k in ('nombre', 'email', 'password')):
                return jsonify({'error': 'Faltan datos requeridos: nombre, email, password'}), 400
            
            nombre = data['nombre']
            email = data['email']
            password = data['password']
            
            # Validaciones básicas
            if len(password) < 6:
                return jsonify({'error': 'La contraseña debe tener al menos 6 caracteres'}), 400
            
            if '@' not in email:
                return jsonify({'error': 'Email inválido'}), 400
            
            usuario = Usuario.crear(nombre, email, password)
            
            # Remover password del response
            if usuario:
                usuario.pop('password', None)
            
            return jsonify(usuario), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @staticmethod
    def listar_usuarios():
        """Obtener todos los usuarios"""
        try:
            usuarios = Usuario.obtener_todos()
            
            # Remover passwords del response
            for usuario in usuarios:
                usuario.pop('password', None)
            
            return jsonify(usuarios), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def obtener_usuario(usuario_id):
        """Obtener usuario por ID"""
        try:
            usuario = Usuario.obtener_por_id(usuario_id)
            
            if not usuario:
                return jsonify({'error': 'Usuario no encontrado'}), 404
            
            # Remover password del response
            usuario.pop('password', None)
            
            return jsonify(usuario), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def actualizar_usuario(usuario_id):
        """Actualizar usuario"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400
            
            nombre = data.get('nombre')
            email = data.get('email')
            password = data.get('password')
            
            # Validaciones
            if email and '@' not in email:
                return jsonify({'error': 'Email inválido'}), 400
            
            if password and len(password) < 6:
                return jsonify({'error': 'La contraseña debe tener al menos 6 caracteres'}), 400
            
            usuario = Usuario.actualizar(usuario_id, nombre, email, password)
            
            if not usuario:
                return jsonify({'error': 'Usuario no encontrado'}), 404
            
            # Remover password del response
            usuario.pop('password', None)
            
            return jsonify(usuario), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @staticmethod
    def eliminar_usuario(usuario_id):
        """Eliminar usuario"""
        try:
            usuario = Usuario.eliminar(usuario_id)
            
            if not usuario:
                return jsonify({'error': 'Usuario no encontrado'}), 404
            
            # Remover password del response
            usuario.pop('password', None)
            
            return jsonify({'message': 'Usuario eliminado correctamente', 'usuario': usuario}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500