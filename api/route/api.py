"""
api.py
"""

from flask import Blueprint, jsonify, request, abort

from api.util.utils import failResponseWrap, successResponseWrap
from api.model.models import *
from api.route.user import api as user_api
from api.route.mock_api import api as mock_api
from api.route.performance import api as performance_api
from api.route.errors import api as error_api
from api.route.useraction import api as useraction_api
from api.route.overview import api as overview_api
from api.route.sdk import api as sdk_api

api = Blueprint('api', __name__, url_prefix='/api')
api.register_blueprint(user_api)
api.register_blueprint(mock_api)
api.register_blueprint(performance_api)
api.register_blueprint(error_api)
api.register_blueprint(useraction_api)
api.register_blueprint(overview_api)
api.register_blueprint(sdk_api)


@api.route('/request', methods=['GET'])
def get_request():
    reqs = RequestData.objects
    return successResponseWrap(reqs)
