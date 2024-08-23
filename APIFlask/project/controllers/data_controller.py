from flask import current_app, jsonify

def get_user_by_id(user_id):
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

        # Si el usuario existe
        if user_data:
            return jsonify({
                "ID_USUARIO": user_data[0],
                "NOMBRE": user_data[1],
                "A_PATERNO": user_data[2],
                # Añadir más campos según la estructura de tu tabla
            }), 200
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500