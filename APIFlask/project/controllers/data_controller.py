from flask import current_app, jsonify


#! Santiago
def login(user_id):
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    try:
        cursor = conn.cursor()

        # Ejecutar la consulta
        query = "SELECT * FROM USUARIOS WHERE ID_USUARIO = %s"
        cursor.execute(query, (user_id,))

        # Obtener resultados
        user_data = cursor.fetchone()


        # Obtener nombres de las columnas
        column_names = [desc[0] for desc in cursor.description]

        # Si el usuario existe
        if user_data:
            # Convertir el resultado en un diccionario
            user_dict = dict(zip(column_names, user_data))
            return jsonify(user_dict), 200
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500