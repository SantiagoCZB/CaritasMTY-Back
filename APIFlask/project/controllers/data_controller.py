from flask import request, jsonify, current_app

def login():
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    # Obtener usuario y contraseña desde el cuerpo de la petición (POST)
    data = request.json
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')

    if not usuario or not contrasena:
        return jsonify({"error": "Usuario y contraseña son requeridos"}), 400

    try:
        cursor = conn.cursor()

        # Ejecutar la consulta
        query = "SELECT * FROM USUARIOS WHERE USUARIO = %s AND CONTRASEÑA = %s"
        cursor.execute(query, (usuario, contrasena))

        # Obtener resultados
        user_data = cursor.fetchone()

        # Si el usuario existe
        if user_data:
            # Obtener nombres de las columnas
            column_names = [desc[0] for desc in cursor.description]
            # Convertir el resultado en un diccionario
            user_dict = dict(zip(column_names, user_data))
            return jsonify({"message": "Login exitoso", "user": user_dict}), 200
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500



#!Rafa
def registrar_evento():
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    data = request.json
    id_usuario = data.get('id_usuario')
    id_evento = data.get('id_evento')

    try:
        cursor = conn.cursor()

        # Verificar si el evento existe y obtener su cupo
        evento_query = "SELECT CUPO FROM EVENTOS WHERE ID_EVENTO = %s"
        cursor.execute(evento_query, (id_evento,))
        evento = cursor.fetchone()

        if not evento:
            return jsonify({"error": "El evento no existe"}), 404

        cupo = evento[0]

        # Contar el número de registros del evento en la tabla USUARIOS_EVENTOS
        count_query = "SELECT COUNT(*) FROM USUARIOS_EVENTOS WHERE ID_EVENTO = %s"
        cursor.execute(count_query, (id_evento,))
        count = cursor.fetchone()[0]

        # Verificar si hay cupo disponible
        if count < cupo:
            # Insertar el nuevo registro en USUARIOS_EVENTOS
            insert_query = "INSERT INTO USUARIOS_EVENTOS (ID_USUARIO, ID_EVENTO, ASISTENCIA) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (id_usuario, id_evento, False))
            conn.commit()
            return jsonify({"message": "Usuario registrado en el evento exitosamente"}), 201
        else:
            return jsonify({"error": "No hay cupo disponible para este evento"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

        