from flask import Blueprint, jsonify, request, abort
from bson import ObjectId
from ua_parser import user_agent_parser
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
        r = user_agent_parser.Parse(request.headers['User-Agent'])
        ip = request.headers['X-Real-Ip']
        os = r['os']['family'] + r['os']['major']
        browser = r['user_agent']['family'] + r['os']['major']
        device = r['device']['family']
        page = request.args.get('page', '')
        newuser = User(ip=ip, os=os, browser=browser,
                       device=device, page=page, tag='TagB')
        newuser.save()
        return successResponseWrap(JSONEncoder().encode(newuser.id))
    except Exception as e:
        print(e)
    return failResponseWrap(msg='Internal Error')


# http://127.0.0.1:5000/api/useraction/all?current=1&pageSize=10
@api.route('/all', methods=['GET'])
def get_user_info_all():
    """查询所有用户
    ---
    tags:
        - 用户细查
    parameters:
        - name: current
          in: query
          type: integer
          description: 当前页
        - name: pageSize
          in: query
          type: integer
          description: 每页数量
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
        - 用户细查
    parameters:
        - name: current
          in: query
          type: integer
          description: 当前页
        - name: pageSize
          in: query
          type: integer
          description: 每页数量
        - name: id
          in: query
          type: string
          description: 用户id
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
