from ddbb.conection import get_conn
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:
    def __init__(self, id=None, nombre=None, email=None, password=None, fecha_creacion=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.fecha_creacion = fecha_creacion
    
    @staticmethod
    def crear_tabla():
        """Crear la tabla de usuarios si no existe"""
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(128) NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
    
    @staticmethod
    def crear(nombre: str, email: str, password: str):
        """Crear un nuevo usuario"""
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("""
                INSERT INTO usuarios (nombre, email, password)
                VALUES (%s, %s, %s)
                RETURNING *;
            """, (nombre, email, password_hash))
            usuario_data = cur.fetchone()
            conn.commit()
            return dict(usuario_data) if usuario_data else None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los usuarios"""
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("SELECT * FROM usuarios;")
            usuarios = cur.fetchall()
            return [dict(usuario) for usuario in usuarios]
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def obtener_por_id(usuario_id):
        """Obtener usuario por ID"""
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("SELECT * FROM usuarios WHERE id=%s;", (usuario_id,))
            usuario = cur.fetchone()
            return dict(usuario) if usuario else None
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def obtener_por_email(email):
        """Obtener usuario por email"""
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("SELECT * FROM usuarios WHERE email=%s;", (email,))
            usuario = cur.fetchone()
            return dict(usuario) if usuario else None
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def actualizar(usuario_id, nombre=None, email=None, password=None):
        """Actualizar usuario"""
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            # Si se proporciona password, encriptarlo
            if password:
                password = generate_password_hash(password, method='pbkdf2:sha256')
            
            cur.execute("""
                UPDATE usuarios SET 
                    nombre = COALESCE(%s, nombre),
                    email = COALESCE(%s, email),
                    password = COALESCE(%s, password)
                WHERE id=%s RETURNING *;
            """, (nombre, email, password, usuario_id))
            usuario = cur.fetchone()
            conn.commit()
            return dict(usuario) if usuario else None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def eliminar(usuario_id):
        """Eliminar usuario"""
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("DELETE FROM usuarios WHERE id=%s RETURNING *;", (usuario_id,))
            usuario = cur.fetchone()
            conn.commit()
            return dict(usuario) if usuario else None
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def verificar_password(password_hash, password):
        """Verificar contraseña"""
        return check_password_hash(password_hash, password)

# Función de conveniencia para crear tabla
def crear_tabla():
    Usuario.crear_tabla()