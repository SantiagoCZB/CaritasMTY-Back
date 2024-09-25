from flask import request, jsonify, current_app
from datetime import time, date

#!Santiago?
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
def registrar():
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

#!César
def cancelar():
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    data = request.json
    id_usuario = data.get('id_usuario')
    id_evento = data.get('id_evento')

    try:
        cursor = conn.cursor()

        # Verificar si el evento existe
        evento_query = "SELECT CUPO FROM EVENTOS WHERE ID_EVENTO = %s"
        cursor.execute(evento_query, (id_evento,))
        evento = cursor.fetchone()

        if not evento:
            return jsonify({"error": "El evento no existe"}), 404

        # Verificar si el usuario está registrado en el evento
        check_user_query = "SELECT COUNT(*) FROM USUARIOS_EVENTOS WHERE ID_USUARIO = %s AND ID_EVENTO = %s"
        cursor.execute(check_user_query, (id_usuario, id_evento))
        is_registered = cursor.fetchone()[0]

        if not is_registered:
            return jsonify({"error": "El usuario no está registrado en el evento"}), 400

        # Eliminar el registro del usuario en USUARIOS_EVENTOS
        delete_query = "DELETE FROM USUARIOS_EVENTOS WHERE ID_USUARIO = %s AND ID_EVENTO = %s"
        cursor.execute(delete_query, (id_usuario, id_evento))

        # Confirmar transacción
        conn.commit()

        return jsonify({"message": "Registro cancelado exitosamente"}), 200

    except Exception as e:
        conn.rollback()  # Revertir la transacción en caso de error
        return jsonify({"error": str(e)}), 500
    

def currentEvents():
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    try:
        cursor = conn.cursor()

        # Consulta para obtener los datos de los eventos
        query = "SELECT * FROM EVENTOS"
        cursor.execute(query)

        # Obtener todos los resultados
        events = cursor.fetchall()

        # Verificar si hay eventos
        if not events:
            return jsonify({"message": "No hay eventos disponibles"}), 404
        
        # Obtener los nombres de las columnas
        column_names = [desc[0] for desc in cursor.description]

        # Convertir cada evento en un diccionario y los valores 'date' y 'time'
        # a cadenas

        eventList = []
        for event in events:
            event_dict = dict(zip(column_names, event))

            for key, value in event_dict.items():
                if isinstance(value, time):
                    event_dict[key] = value.strftime('%H:%M:%S')
                elif isinstance(value, date):
                    event_dict[key] = value.strftime('%Y-%m-%d')
            eventList.append(event_dict)

        return jsonify({"Eventos": eventList}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_users():
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    try:
        cursor = conn.cursor()

        # Consulta para obtener a todos los usuarios
        query = "SELECT ID_USUARIO, NOMBRE, A_PATERNO, A_MATERNO, \
                ID_TIPO_USUARIO, PESO, ALTURA, PRESION, USUARIO FROM USUARIOS"
        cursor.execute(query)

        # Obtener todos los resultados
        users = cursor.fetchall()

        # Verificar si hay usuarios
        if not users:
            return jsonify({"message": "No hay usuarios registrados"}), 404
        
        # Obtener los nombres de las columnas
        column_names = [desc[0] for desc in cursor.description]

        # Convertir cada usuario en un diccionario
        # Un diccionario es una estructura de datos que
        # almacena pares de clave-valor.
        userList = [dict(zip(column_names, user)) for user in users]

        return jsonify({"Usuarios": userList}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#!Kevin
def get_recompensas_tienda():
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    try:
        cursor = conn.cursor()

        # Obtener todas las recompensas disponibles en la tienda
        recompensas_query = "SELECT ID_RECOMPENSA, NOMBRE, DESCRIPCION, COSTO FROM RECOMPENSAS"
        cursor.execute(recompensas_query)
        recompensas = cursor.fetchall()

        recompensas_list = []
        for recompensa in recompensas:
            recompensas_list.append({
                "id_recompensa": recompensa.ID_RECOMPENSA,
                "nombre": recompensa.NOMBRE,
                "descripcion": recompensa.DESCRIPCION,
                "costo": recompensa.COSTO
            })

        return jsonify({"recompensas": recompensas_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        
        
#Emmanuel
def mis_eventos(id_usuario):
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    try:
        cursor = conn.cursor()

        # Consulta SQL para obtener todos los datos de los eventos a los que el usuario está inscrito
        query = """
        SELECT E.ID_EVENTO, E.TITULO, E.FECHA, E.HORA, E.DESCRIPCION, E.CUPO, E.PUNTOS, E.TIPO_EVENTO 
        FROM USUARIOS_EVENTOS UE
        JOIN EVENTOS E ON UE.ID_EVENTO = E.ID_EVENTO
        WHERE UE.ID_USUARIO = %s
        """
        cursor.execute(query, (id_usuario,))

        # Obtener los resultados
        eventos = cursor.fetchall()

        # Verificar si hay eventos
        if not eventos:
            return jsonify({"message": "El usuario no está registrado en ningún evento"}), 404

        # Obtener los nombres de las columnas de la consulta
        column_names = [desc[0] for desc in cursor.description]

        # Convertir cada evento en un diccionario, formatear las fechas y horas como cadenas
        eventList = []
        for event in eventos:
            event_dict = dict(zip(column_names, event))

            # Convertir 'date' y 'time' a formato de cadena
            for key, value in event_dict.items():
                if isinstance(value, time):
                    event_dict[key] = value.strftime('%H:%M:%S')
                elif isinstance(value, date):
                    event_dict[key] = value.strftime('%Y-%m-%d')

            eventList.append(event_dict)

        return jsonify({"Eventos": eventList}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
def verificar_registro():
    # Obtener la conexión a la base de datos desde la configuración de la aplicación
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    # Obtener los datos del cuerpo de la solicitud
    data = request.json
    id_usuario = data.get('id_usuario')
    id_evento = data.get('id_evento')

    try:
        cursor = conn.cursor()

        # Verificar si el registro existe en la tabla USUARIOS_EVENTOS
        query = "SELECT 1 FROM USUARIOS_EVENTOS WHERE ID_USUARIO = %s AND ID_EVENTO = %s"
        cursor.execute(query, (id_usuario, id_evento))
        registro = cursor.fetchone()

        # Si se encuentra el registro, devolver true, si no, devolver false
        if registro:
            return jsonify({"exists": True}), 200
        else:
            return jsonify({"exists": False}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500