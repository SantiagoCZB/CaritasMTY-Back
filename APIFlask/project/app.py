from flask import Flask
from flask_cors import CORS
from db import get_db_connection
from routes.main_routes import bp as main_bp
from flasgger import Swagger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app():
    app = Flask(__name__)

    # Limitador Global de Peticiones
    limiter = Limiter(
        get_remote_address, 
        app = app, 
        default_limits=["20000 per day", "5000 per hour"]
    )

    # Asociamos swagger al app 
    swagger = Swagger(app, template={
        "info": {
            "title": "API Gestor de salud y bienestar",
            "description": "REST API para la materia TC2007B",
            "version": "1.0.0"
        }
    })

    CORS(app)
    
    # Registrar el blueprint
    app.register_blueprint(main_bp)

    # Inicializar la conexión a la base de datos
    app.config['DB_CONNECTION'] = get_db_connection()

    if __name__ == "__main__":
        return app