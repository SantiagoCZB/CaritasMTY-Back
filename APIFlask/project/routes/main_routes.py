from flask import Blueprint
from controllers import data_controller

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
 return "API RealMadSwift ⚽"

@bp.route('/data', methods=['GET'])
def get_data():
    return data_controller.get_data()

@bp.route('/data', methods=['POST'])
def post_data():
    return data_controller.post_data()