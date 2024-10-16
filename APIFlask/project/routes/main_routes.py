from flask import Blueprint
from controllers.data_controller import *
from requestLimit import limiter

bp = Blueprint('main', __name__)

@bp.route('/')
@limiter.limit("100 per minute")
def index():
  return "API RealMadSwift ⚽"

@bp.route('/login', methods=['POST'])
@limiter.limit("100 per minute")
def loginRoute():
    return login()


# Probamos en cURL
# curl -X POST -k -H "Content-Type: application/json" -d "{\"id_usuario\":3,\"id_evento\":3}" https://realmadswift.tc2007b.tec.mx:10206/registrar_evento
@bp.route('/registrar_evento', methods=['POST'])
@limiter.limit("100 per minute")
def registrar_evento():
   return registrar()

# Probamos en cURL así (Después del registrar evento. Escapar comillas dentro del formato JSON con '\'):
# curl -X DELETE -k -H "Content-Type: application/json" -d "{\"id_usuario\":3,\"id_evento\":3}" https://realmadswift.tc2007b.tec.mx:10206/cancelar_registro
@bp.route('/cancelar_registro', methods=['DELETE'])
@limiter.limit("100 per minute")
def cancelar_registro():
   """
    Cancela el registro de un usuario en un evento
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            ID_USUARIO:
              type: integer
              description: ID del usuario
            ID_EVENTO:
              type: integer
              description: ID del evento
    responses:
      200:
        description: Registro cancelado exitosamente
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Mensaje de respuesta
      400:
        description: El usuario no está registrado en el evento
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensaje de error
      404:
        description: El evento no existe
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensaje de error
      429:
        description: "Demasiadas Solicitudes a la API"
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Demasiadas Solicitudes"
      500:
        description: Error de conexión o consulta a la base de datos
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensaje de error
   """
   return cancelar()

@bp.route('/users', methods=['GET'])
@limiter.limit("100 per minute")
def users():
   """
    Despliega todos los usuarios disponibles desde la base de datos
    ---
    responses:
      200:
        description: "Lista de usuarios"
        content:
          application/json:    
            schema:
              type: object
              properties:
                Usuarios:
                  type: array
                  items:
                    type: object
                    properties:
                      ID_USUARIO:
                        type: integer
                        description: "ID del usuario"
                      NOMBRE:
                        type: string
                        description: "Nombre del usuario"
                      A_PATERNO:
                        type: string
                        description: "Apellido paterno del usuario"
                      A_MATERNO:
                        type: string
                        description: "Apellido materno del usuario"
                      USUARIO:
                        type: string
                        description: "Nombre de usuario"
                      ID_TIPO_USUARIO:
                        type: string
                        description: "ID del tipo de usuario"
                      ALTURA:
                        type: number
                        format: float
                        description: "Altura del usuario (en metros)"
                      PESO:
                        type: number
                        format: float
                        description: "Peso del usuario (en kilogramos)"
                      PRESION:
                        type: string
                        description: "Presión arterial del usuario"
      404:
        description: "No hay usuarios disponibles"
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "No hay usuarios disponibles"
      429:
        description: "Demasiadas Solicitudes a la API"
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Demasiadas Solicitudes"
      500:
        description: "Database connection or query error"
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: "Mensaje de error"
   """
   return get_users()

@bp.route('/<int:id_usuario>/events', methods=['GET'])
@limiter.limit("100 per minute")
def events(id_usuario):
   """
    Despliega todos los eventos disponibles desde la base de datos para el usuario correspondiente a la id
    ---
    responses:
      200:
        description: "Muestra correctamente una Lista de eventos"
        content:
          application/json:
            schema:
              type: object
              properties:
                Eventos:
                  type: array
                  items:
                    type: object
                    properties:
                      ID_EVENTO:
                        type: integer
                        description: "ID del evento"
                      TITULO:
                        type: string
                        description: "Título del evento"
                      FECHA:
                        type: string
                        format: date
                        description: "Fecha del evento"
                      HORA:
                        type: string
                        format: time
                        description: "Hora del evento"
                      PUNTOS:
                        type: string
                        format: time
                        description: "Puntos del evento"
                      TIPO_EVENTO:
                        type: string
                        format: time
                        description: "Tipo del evento"
                      CUPO:
                        type: string
                        format: time
                        description: "Cupo para el evento"
                      DESCRIPCION:
                        type: string
                        format: time
                        description: "Descripción del evento"
      404:
        description: "No hay eventos disponibles"
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "No hay eventos disponibles"
      429:
        description: "Demasiadas Solicitudes a la API"
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Demasiadas Solicitudes"
      500:
        description: "Error de la base de datos o de consulta"
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: "Mensaje de error"
   """
   return currentEvents(id_usuario)

@bp.route('/<int:id_usuario>/mis-eventos', methods=['GET'])
@limiter.limit("100 per minute")
def mis_eventosRoute(id_usuario):
   return mis_eventos(id_usuario)
 
@bp.route('/verificar_registro', methods=['POST'])
@limiter.limit("100 per minute")
def verificar_registroRoute():
   return verificar_registro()
 
@bp.route('/<int:id_usuario>/retos', methods=['GET'])
@limiter.limit("100 per minute")
def retos(id_usuario):
  return obtenerRetos(id_usuario)

@bp.route('/<int:id_usuario>/mis-retos', methods=['GET'])
@limiter.limit("100 per minute")
def mis_retosRoute(id_usuario):
   return mis_retos(id_usuario)
 
@bp.route('/registrar_reto', methods=['POST'])
@limiter.limit("100 per minute")
def registrar_reto():
   return registrarReto()

@bp.route('/cancelar_reto', methods=['DELETE'])
@limiter.limit("100 per minute")
def cancelar_registro_reto():
  return cancelarReto()

@bp.route('/verificar_reto', methods=['POST'])
@limiter.limit("100 per minute")
def verificar_registro_retoRoute():
   return verificar_registroReto()
 
@bp.route('/recompensas', methods=['POST'])
@limiter.limit("100 per minute")
def recompensasRoute():
   return obtenerRecompensas()

@bp.route('/comprar', methods=['POST'])
@limiter.limit("100 per minute")
def comprarRoute():
   return comprarRecompensa()
 
 
@bp.route('/puntos-user', methods=['POST'])
@limiter.limit("100 per minute")
def puntosUserRoute():
   return get_puntos_usuario()