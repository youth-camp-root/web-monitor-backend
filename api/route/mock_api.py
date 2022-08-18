from flask import Blueprint, jsonify, request

from api.util.utils import successResponseWrap
from api.mock.data_generator import UserMaterial, ErrorMaterial, RequestMaterial
from ..mock.mock_data_forger import user_forger, request_forger, error_forger, delete_collection

api = Blueprint('mock_api', __name__, url_prefix="/mock")


@api.route('/users', methods=['GET'])
def get_mocked_users():
    """生成 User mock 临时数据并返回
    ---
    tags:
        - mock数据
    """
    users = UserMaterial().generate_user_data()
    return successResponseWrap(users)


@api.route('/requests', methods=['GET'])
def get_mocked_requests():
    """生成 Request mock 临时数据并返回
    ---
    tags:
        - mock数据
    """
    reqs = RequestMaterial().generate_request_data(None)
    return successResponseWrap(reqs)


@api.route('/errors', methods=['GET'])
def get_mocked_errors():
    """生成 Error mock 临时数据并返回
    ---
    tags:
        - mock数据
    """
    errors = ErrorMaterial().generate_error_data(None)
    return successResponseWrap(errors)


@api.route('/forge/user/<amount>', methods=['POST'])
def mock_users(amount):
    """生成 User mock 数据并注入到数据库
    ---
    tags:
        - mock数据
    parameters:
        - name: amount
          in: path
          type: string
          required: true
        - name: drop-first
          in: query
          type: string
          required: false
    """
    check_drop = request.args.get('drop-first')
    msg = ''
    if check_drop == 'yes':
        msg = delete_collection('User')
    if user_forger(amount):
        return jsonify({'data': msg + ' User mock data forged', 'status': True, 'code': 200})
    else:
        return jsonify({'data': msg + ' User mock data forge failed', 'status': False, 'code': 400})


@api.route('/forge/request/<amount>', methods=['POST'])
def mock_requests(amount):
    """生成 Request mock 数据并注入到数据库
    ---
    tags:
        - mock数据
    parameters:
        - name: amount
          in: path
          type: string
          required: true
        - name: drop-first
          in: query
          type: string
          required: false
    """
    check_drop = request.args.get('drop-first')
    msg = ''
    if check_drop == 'yes':
        msg = delete_collection('RequestData')
    if request_forger(amount):
        return jsonify({'data': msg + ' Request mock data forged', 'status': True, 'code': 200})
    else:
        return jsonify({'data': msg + ' Request mock data forge failed', 'status': False, 'code': 400})


@api.route('/forge/error/<amount>', methods=['POST'])
def mock_errors(amount):
    """生成 Error mock 数据并注入到数据库
    ---
    tags:
        - mock数据
    parameters:
        - name: amount
          in: path
          type: string
          required: true
        - name: drop-first
          in: query
          type: string
          required: false
    """
    check_drop = request.args.get('drop-first')
    msg = ''
    if check_drop == 'yes':
        msg = delete_collection('ErrorData')
    if error_forger(amount):
        return jsonify({'data': msg + ' Error mock data forged', 'status': True, 'code': 200})
    else:
        return jsonify({'data': msg + ' Error mock data forge failed', 'status': False, 'code': 400})

