from flask import Blueprint
from controllers.data_controller import get_user_by_id

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
 return "API RealMadSwift ⚽"

@bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    return get_user_by_id(user_id)




