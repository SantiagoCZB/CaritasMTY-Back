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

        # Hash de la contraseña ingresada en formato hexadecimal
        hash_contrasena = f"{contrasena}".encode('utf-8').hex()

        # Ejecutar la consulta
        query = """
        SELECT * 
        FROM USUARIOS 
        WHERE USUARIO = %s AND 
        CONVERT(VARCHAR(64), CONTRASEÑA, 2) = %s
        """
        cursor.execute(query, (usuario, hash_contrasena))

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

        # Consulta para obtener los eventos que aún no han ocurrido
        query = """
        SELECT * 
        FROM EVENTOS 
        WHERE (FECHA > CAST(GETDATE() AS DATE)) 
        OR (FECHA = CAST(GETDATE() AS DATE) AND HORA > CAST(GETDATE() AS TIME))
        """
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
def obtenerRecompensas():
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500
    
    data = request.json
    id_usuario = data.get('id_usuario')

    try:
        cursor = conn.cursor()

        # Consulta para obtener todas las recompensas con NOMBRE, COSTO, DESCRIPCION y RESTANTES
        recompensas_query = "SELECT ID_RECOMPENSA, NOMBRE, DESCRIPCION, COSTO, RESTANTES FROM RECOMPENSAS"
        cursor.execute(recompensas_query)
        recompensas = cursor.fetchall()

        # Verificar si hay recompensas
        if not recompensas:
            return jsonify({"message": "No hay recompensas disponibles"}), 404

        # Obtener las recompensas ya compradas por el usuario
        compradas_query = """
        SELECT ID_RECOMPENSA 
        FROM USUARIOS_RECOMPENSAS 
        WHERE ID_USUARIO = %s
        """
        cursor.execute(compradas_query, (id_usuario,))
        recompensas_compradas = cursor.fetchall()

        # Convertir las recompensas compradas en un conjunto para fácil búsqueda
        recompensas_compradas_set = {row[0] for row in recompensas_compradas}

        # Generar la lista de recompensas con el campo extra "COMPRADO" y excluyendo las que tienen RESTANTES = 0
        recompensasList = []
        for recompensa in recompensas:
            id_recompensa, nombre, descripcion, costo, restantes = recompensa  # Extraemos los campos incluyendo RESTANTES
            
            # Si el valor de RESTANTES es 0, no incluir la recompensa en la lista
            if restantes == 0:
                continue

            # Crear un diccionario para la recompensa
            recompensa_dict = {
                "ID_RECOMPENSA": id_recompensa,
                "NOMBRE": nombre,
                "DESCRIPCION": descripcion,
                "COSTO": costo,
                "RESTANTES": restantes,  # Incluimos el campo RESTANTES en el JSON
                "COMPRADO": id_recompensa in recompensas_compradas_set  # Si la recompensa está comprada, poner COMPRADO: true
            }
            recompensasList.append(recompensa_dict)

        return jsonify({"Recompensas": recompensasList}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

        
        
#Emmanuel
def mis_eventos(id_usuario):
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    try:
        cursor = conn.cursor()

        # Consulta SQL para obtener solo los eventos con asistencia en 0
        query = """
        SELECT E.ID_EVENTO, E.TITULO, E.FECHA, E.HORA, E.DESCRIPCION, E.CUPO, E.PUNTOS, E.TIPO_EVENTO 
        FROM USUARIOS_EVENTOS UE
        JOIN EVENTOS E ON UE.ID_EVENTO = E.ID_EVENTO
        WHERE UE.ID_USUARIO = %s
        AND UE.ASISTENCIA = 0
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
    
        
def obtenerRetos():
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    try:
        cursor = conn.cursor()

        # Consulta para obtener todos los registros de la tabla RETOS
        query = "SELECT * FROM RETOS"
        cursor.execute(query)

        # Obtener todos los resultados
        retos = cursor.fetchall()

        # Verificar si hay retos
        if not retos:
            return jsonify({"message": "No hay retos disponibles"}), 404

        # Obtener los nombres de las columnas
        column_names = [desc[0] for desc in cursor.description]

        # Convertir cada registro de RETOS en un diccionario
        retosList = []
        for reto in retos:
            reto_dict = dict(zip(column_names, reto))
            retosList.append(reto_dict)

        return jsonify({"Retos": retosList}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def mis_retos(id_usuario):
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    try:
        cursor = conn.cursor()

        # Consulta SQL para obtener los retos que no han sido cumplidos (CUMPLIDO = 0)
        query = """
        SELECT R.ID_RETO, R.NOMBRE, R.DESCRIPCION, R.PUNTAJE
        FROM USUARIOS_RETOS UR
        JOIN RETOS R ON UR.ID_RETO = R.ID_RETO
        WHERE UR.ID_USUARIO = %s
        AND UR.CUMPLIDO = 0
        """
        cursor.execute(query, (id_usuario,))

        # Obtener los resultados
        retos = cursor.fetchall()

        # Verificar si hay retos
        if not retos:
            return jsonify({"message": "El usuario no tiene retos pendientes"}), 404

        # Obtener los nombres de las columnas de la consulta
        column_names = [desc[0] for desc in cursor.description]

        # Convertir cada reto en un diccionario
        retosList = []
        for reto in retos:
            reto_dict = dict(zip(column_names, reto))
            retosList.append(reto_dict)

        return jsonify({"Retos": retosList}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def registrarReto():
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    data = request.json
    id_usuario = data.get('id_usuario')
    id_reto = data.get('id_reto')

    try:
        cursor = conn.cursor()

        # Verificar si el reto ya está registrado para el usuario
        check_query = "SELECT COUNT(*) FROM USUARIOS_RETOS WHERE ID_USUARIO = %s AND ID_RETO = %s"
        cursor.execute(check_query, (id_usuario, id_reto))
        already_registered = cursor.fetchone()[0]

        if already_registered:
            return jsonify({"error": "El usuario ya está registrado en este reto"}), 400

        # Insertar el nuevo registro en USUARIOS_RETOS con CUMPLIDO en 0
        insert_query = "INSERT INTO USUARIOS_RETOS (ID_USUARIO, ID_RETO, CUMPLIDO) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (id_usuario, id_reto, 0))
        conn.commit()

        return jsonify({"message": "Usuario registrado en el reto exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def cancelarReto():
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    data = request.json
    id_usuario = data.get('id_usuario')
    id_reto = data.get('id_reto')

    try:
        cursor = conn.cursor()

        # Verificar si el usuario está registrado en el reto
        check_user_query = "SELECT COUNT(*) FROM USUARIOS_RETOS WHERE ID_USUARIO = %s AND ID_RETO = %s"
        cursor.execute(check_user_query, (id_usuario, id_reto))
        is_registered = cursor.fetchone()[0]

        if not is_registered:
            return jsonify({"error": "El usuario no está registrado en el reto"}), 400

        # Eliminar el registro del usuario en USUARIOS_RETOS
        delete_query = "DELETE FROM USUARIOS_RETOS WHERE ID_USUARIO = %s AND ID_RETO = %s"
        cursor.execute(delete_query, (id_usuario, id_reto))

        # Confirmar transacción
        conn.commit()

        return jsonify({"message": "Registro cancelado exitosamente"}), 200

    except Exception as e:
        conn.rollback()  # Revertir la transacción en caso de error
        return jsonify({"error": str(e)}), 500

    
    
def verificar_registroReto():
    # Obtener la conexión a la base de datos desde la configuración de la aplicación
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    # Obtener los datos del cuerpo de la solicitud
    data = request.json
    id_usuario = data.get('id_usuario')
    id_reto = data.get('id_reto')

    try:
        cursor = conn.cursor()

        # Verificar si el registro existe en la tabla USUARIOS_RETOS
        query = "SELECT 1 FROM USUARIOS_RETOS WHERE ID_USUARIO = %s AND ID_RETO = %s"
        cursor.execute(query, (id_usuario, id_reto))
        registro = cursor.fetchone()

        # Si se encuentra el registro, devolver true, si no, devolver false
        if registro:
            return jsonify({"exists": True}), 200
        else:
            return jsonify({"exists": False}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
from flask import request, jsonify, current_app


def comprarRecompensa():
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500
    
    data = request.json
    id_usuario = data.get('id_usuario')
    id_recompensa = data.get('id_recompensa')

    try:
        cursor = conn.cursor()

        # 1. Verificar si el usuario ya ha comprado la recompensa
        query_ya_comprada = """
        SELECT * FROM USUARIOS_RECOMPENSAS WHERE ID_USUARIO = %s AND ID_RECOMPENSA = %s
        """
        cursor.execute(query_ya_comprada, (id_usuario, id_recompensa))
        recompensa_comprada = cursor.fetchone()

        if recompensa_comprada:
            return jsonify({"message": "Ya has comprado esta recompensa"}), 400

        # 2. Obtener el puntaje del usuario
        query_puntaje_usuario = """
        SELECT PUNTAJE FROM USUARIOS WHERE ID_USUARIO = %s
        """
        cursor.execute(query_puntaje_usuario, (id_usuario,))
        resultado_usuario = cursor.fetchone()

        if resultado_usuario is None:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        puntaje_usuario = resultado_usuario[0]

        # 3. Obtener el costo y restantes de la recompensa
        query_recompensa = """
        SELECT COSTO, RESTANTES FROM RECOMPENSAS WHERE ID_RECOMPENSA = %s
        """
        cursor.execute(query_recompensa, (id_recompensa,))
        resultado_recompensa = cursor.fetchone()

        if resultado_recompensa is None:
            return jsonify({"error": "Recompensa no encontrada"}), 404

        costo_recompensa, restantes_recompensa = resultado_recompensa

        # 4. Verificar si el usuario tiene suficientes monedas
        if puntaje_usuario < costo_recompensa:
            return jsonify({"message": "No tienes suficientes monedas"}), 400

        # 5. Verificar si quedan recompensas disponibles
        if restantes_recompensa <= 0:
            return jsonify({"message": "No quedan recompensas disponibles"}), 400

        # 6. Realizar las actualizaciones:
        # Restar el costo de la recompensa al puntaje del usuario
        update_puntaje_usuario = """
        UPDATE USUARIOS SET PUNTAJE = PUNTAJE - %s WHERE ID_USUARIO = %s
        """
        cursor.execute(update_puntaje_usuario, (costo_recompensa, id_usuario))

        # Restar 1 a las recompensas restantes
        update_recompensa_restantes = """
        UPDATE RECOMPENSAS SET RESTANTES = RESTANTES - 1 WHERE ID_RECOMPENSA = %s
        """
        cursor.execute(update_recompensa_restantes, (id_recompensa,))

        # Registrar la compra en la tabla USUARIOS_RECOMPENSAS
        insert_compra = """
        INSERT INTO USUARIOS_RECOMPENSAS (ID_USUARIO, ID_RECOMPENSA) VALUES (%s, %s)
        """
        cursor.execute(insert_compra, (id_usuario, id_recompensa))

        # Confirmar los cambios en la base de datos
        conn.commit()

        return jsonify({"message": "Compra realizada con éxito"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def get_puntos_usuario():
    conn = current_app.config['DB_CONNECTION']
    if conn is None:
        return jsonify({"error": "No database connection available"}), 500

    # Obtener el JSON del body
    data = request.get_json()

    # Asegurarse de que el campo id_usuario fue proporcionado
    id_usuario = data.get('id_usuario')
    
    if not id_usuario:
        return jsonify({"error": "id_usuario is required"}), 400
    
    try:
        cursor = conn.cursor()

        # Consulta para obtener el puntaje del usuario
        query = "SELECT PUNTAJE FROM USUARIOS WHERE ID_USUARIO = %s"
        cursor.execute(query, (id_usuario,))
        puntos = cursor.fetchone()
        
        if puntos:
            return jsonify({"puntos": puntos[0]}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()