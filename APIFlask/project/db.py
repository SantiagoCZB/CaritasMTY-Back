import pymssql
from dotenv import load_dotenv
import os

# Cargar las variables desde el archivo .env
load_dotenv()

def get_db_connection():
    try:
        conn = pymssql.connect(
            server=os.getenv('DB_SERVER'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        
        return None

