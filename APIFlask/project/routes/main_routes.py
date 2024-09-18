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