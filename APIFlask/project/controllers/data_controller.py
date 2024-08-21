from flask import jsonify, request

def get_data():
    data = {
        'message': 'Hola desde la API',
        'status': 'success'
    }
    return jsonify(data)

def post_data():
    incoming_data = request.json
    return jsonify({'received': incoming_data, 'status': 'success'})