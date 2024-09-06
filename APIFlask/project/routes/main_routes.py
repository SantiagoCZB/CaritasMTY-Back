from flask import Blueprint
from controllers.data_controller import login

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
 return "API RealMadSwift ⚽"

@bp.route('/<user_id>', methods=['GET'])
def login(user_id):
    return login(user_id)




