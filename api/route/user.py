from flask import Blueprint, jsonify, request, abort
from bson import ObjectId

from api.util.utils import failResponseWrap, successResponseWrap
from api.model.models import *

api = Blueprint('user', __name__, url_prefix='/user')


@api.route('/', methods=['GET'])
def get_users():
    """列出所有用户
    ---
    tags:
        - 用户
    description:
        用户列表
    """
    users = User.objects
    return successResponseWrap(users)


@api.route('/<userID>', methods=['GET'])
def get_user_info(userID):
    """查询某个特定用户
    ---
    tags:
        - 用户
    parameters:
        - name: id
          in: query
          type: string
          required: true
    """

    try:
        user = User.objects(_id=ObjectId(userID)).first()
        if not user:
            return failResponseWrap(msg='User not found')

        user_events = RequestData.objects(user=ObjectId(userID))
        user_errors = ErrorData.objects(user=ObjectId(userID))

        return successResponseWrap({'user': user, 'events': user_events, 'errors': user_errors})

    except Exception as e:
        print(e)
        return failResponseWrap(msg='Internal Error')
