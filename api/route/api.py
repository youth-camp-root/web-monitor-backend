"""
api.py
"""

from flask import Blueprint, jsonify, request, abort
from bson.objectid import ObjectId

from api.util.utils import failResponseWrap, successResponseWrap
from api.model.models import *
from api.route.user import api as user_api
from api.route.mock_api import api as mock_api

api = Blueprint('api', __name__, url_prefix='/api')
api.register_blueprint(user_api)
api.register_blueprint(mock_api)


@api.route('/request', methods=['GET'])
def get_request():
    reqs = RequestData.objects
    return successResponseWrap(reqs)


@api.route('/errors', methods=['GET'])
def get_errors():
    category = request.args.get('category')
    userID = request.args.get('userid')

    if category:
        errors = ErrorData.objects(category=category)
    elif userID:
        errors = ErrorData.objects(user=ObjectId(userID))
    else:
        errors = ErrorData.objects

    if not errors:
        return failResponseWrap(msg='User not found')
    else:
        return successResponseWrap([error.to_dict(withUserInfo=True) for error in errors])
