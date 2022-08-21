from flask import Blueprint, jsonify, request, abort
from bson import ObjectId
import random
from api.util.utils import failResponseWrap, successResponseWrap
from api.model.models import *
import json
api = Blueprint('useraction', __name__, url_prefix='/useraction')


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@api.route('/login', methods=['GET'])
def login():
    try:
        ip = request.remote_addr
        os = request.args.get('os')
        browser = request.args.get('browser')
        device = request.args.get('device')
        print(os)
        print(device)
        print(browser)
        newuser = User(ip=ip, os=os, browser=browser,
                       device=device, page='', tag='TagB')
        newuser.save()
        return successResponseWrap(JSONEncoder().encode(newuser.id))
    except Exception as e:
        print(e)
    return failResponseWrap(msg='Internal Error')


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

# http://127.0.0.1:5000/api/useraction/all?current=1&pageSize=10


@api.route('/all', methods=['GET'])
def get_user_info_all():
    """查询所有用户
    ---
    tags:
        - 用户
    parameters:
        - current: number;
          pageSize: number;
          required: true;
    """
    items_per_page = request.args.get('pageSize')
    page_nb = request.args.get('current')
    offset = (int(page_nb) - 1) * int(items_per_page)
    try:
        list = User.objects.skip(int(offset)).limit(int(items_per_page))
        total = int(int(User.objects.count()) / int(items_per_page))
        return successResponseWrap({'list': list, 'total': total})

    except Exception as e:
        print(e)
        return failResponseWrap(msg='Internal Error')

# http://127.0.0.1:5000/api/useraction/one?current=1&pageSize=10&id=62fe4465694e1f2a8ca0cc3b


@api.route('/one', methods=['GET'])
def get_user_info_one():
    """查询某个特定用户
    ---
    tags:
        - 用户
    parameters:
        - id: string;
          current: number;
          pageSize: number;
          required: true;
    """
    id = request.args.get('id')
    items_per_page = request.args.get('pageSize')
    page_nb = request.args.get('current')
    offset = (int(page_nb) - 1) * int(items_per_page)
    try:
        user = User.objects(_id=ObjectId(id)).first()
        temp = RequestData.objects(user=ObjectId(id)).skip(
            int(offset)).limit(int(items_per_page))
        list = []
        for val in temp:
            k = user
            k.page = val.targetURL
            list.append(k)
        total = int(int(RequestData.objects(
            user=ObjectId(id)).count()) / int(items_per_page))
        return successResponseWrap({'list': list, 'total': total})

    except Exception as e:
        print(e)
        return failResponseWrap(msg='Internal Error')
