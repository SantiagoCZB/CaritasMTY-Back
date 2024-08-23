from flask import Flask
from flask_cors import CORS
from db import get_db_connection

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Inicializar la conexión a la base de datos
    app.config['DB_CONNECTION'] = get_db_connection()

    return app