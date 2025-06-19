import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    """
    Obtiene una conexión a la base de datos PostgreSQL
    """
    try:
        conn = psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST', '203.161.35.27'),
            port=os.environ.get('POSTGRES_PORT', 5872),
            database=os.environ.get('POSTGRES_DB', 'postgres'),
            user=os.environ.get('POSTGRES_USER', 'postgres'),
            password=os.environ.get('POSTGRES_PASSWORD', '123456789')
        )
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        raise e