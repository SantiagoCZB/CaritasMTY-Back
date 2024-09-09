from flask import Blueprint
from controllers.data_controller import login

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




