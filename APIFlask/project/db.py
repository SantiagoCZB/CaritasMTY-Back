import pymssql
from dotenv import load_dotenv
import os

# Cargar las variables desde el archivo .env
load_dotenv()

def get_db_connection():
    try:
        
        print(f"DB_SERVER: {os.getenv('DB_SERVER')}")
        print(f"DB_USER: {os.getenv('DB_USER')}")
        print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
        print(f"DB_NAME: {os.getenv('DB_NAME')}")
        conn = pymssql.connect(
            server=os.getenv('DB_SERVER'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=1433
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        
        return None

