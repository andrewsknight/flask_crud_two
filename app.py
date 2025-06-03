import os
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from ddbb.conection import get_conn

load_dotenv()

app = Flask(__name__)

# Configuración de conexión


# Crear tabla si no existe (puedes ejecutar esto 1 sola vez)

def crear_tabla():
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

# --------- ENDPOINTS CRUD -----------

# Crear usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nombre = data['nombre']
    email = data['email']
    
    # guardamos el password encryptado en la base de datos
    password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            INSERT INTO usuarios (nombre, email, password)
            VALUES (%s, %s, %s)
            RETURNING *;
        """, (nombre, email, password))
        usuario = cur.fetchone()
        conn.commit()
        return jsonify(usuario), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

# Leer todos los usuarios
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM usuarios;")
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(usuarios)

# Leer usuario por ID
@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM usuarios WHERE id=%s;", (usuario_id,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

# Actualizar usuario
@app.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        UPDATE usuarios SET nombre=%s, email=%s, password=%s
        WHERE id=%s RETURNING *;
    """, (nombre, email, password, usuario_id))
    usuario = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

# Eliminar usuario
@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("DELETE FROM usuarios WHERE id=%s RETURNING *;", (usuario_id,))
    usuario = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if usuario:
        return jsonify({'deleted': usuario})
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

# --------------------------------------

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
