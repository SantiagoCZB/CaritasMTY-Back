from flask import Blueprint
from controllers.data_controller import *

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
 return "API RealMadSwift ⚽"

@bp.route('/login', methods=['POST'])
def loginRoute():
    return login()

@bp.route('/<registrar_evento>', methods=['POST'])
def registrar_evento():
   return registrar_evento()

@bp.route('/users', methods=['GET'])
def users():
    return get_users()

@bp.route('/events', methods=['GET'])
def events():
   return currentEvents()

@bp.route('/<int:id_usuario>/mis-eventos', methods=['GET'])
def mis_eventosRoute(id_usuario):
    return mis_eventos(id_usuario)