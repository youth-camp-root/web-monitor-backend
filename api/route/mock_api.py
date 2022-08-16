from flask import Blueprint, jsonify

from api.util.utils import successResponseWrap
from api.mock.data_generator import UserMaterial, ErrorMaterial, RequestMaterial

api = Blueprint('mock_api', __name__, url_prefix="/mock")


@api.route('/users', methods=['GET'])
def get_mocked_users():
    users = UserMaterial().generate_user_data()
    return successResponseWrap(users)


@api.route('/requests', methods=['GET'])
def get_mocked_requests():
    reqs = RequestMaterial().generate_request_data(None)
    return successResponseWrap(reqs)


@api.route('/errors', methods=['GET'])
def get_mocked_errors():
    errors = ErrorMaterial().generate_error_data(None)
    return successResponseWrap(errors)

