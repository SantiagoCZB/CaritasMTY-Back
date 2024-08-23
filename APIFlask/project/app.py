from flask import Flask
from flask_cors import CORS
from db import get_db_connection
from routes.main_routes import bp as main_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.register_blueprint(main_bp)

    # Inicializar la conexión a la base de datos
    app.config['DB_CONNECTION'] = get_db_connection()

    return app