from flask import Flask, jsonify, request
from flask_cors import CORS

apiflask = Flask(__name__)
CORS(apiflask)

@apiflask.route('/')
def index():
    return "API RealMadSwift ⚽"

@apiflask.route('/data', methods=['GET'])
def get_data():
    # Aquí se definen los datos para enviar a la apiflask
    data = {
        'message': 'Hola desde la API',
        'status': 'success'
    }
    return jsonify(data)

    # Probar con: curl http://127.0.0.1:5000/data
    # En el CMD


@apiflask.route('/data', methods=['POST'])
def post_data():
    # Datos que se reciben de la apiflask
    incoming_data = request.json
    return jsonify({'received': incoming_data, 'status': 'success'})

    # Probar con: curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d "{\"username\": \"testUser\", \"score\": 42}"
    # En el CMD

if __name__ == '__main__':
    apiflask.run(debug=True, host='0.0.0.0', port=5000)