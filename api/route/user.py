from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, abort
from bson import ObjectId
from api.mock.mock_data_forger import pageLoad_forger

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
        - name: userID
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


@api.route('/<userID>/stat', methods=["GET"])
def get_user_stat(userID):
    """查询特定用户的图表统计数据
    ---
    description:
        用户展示三张图表。
        1. 页面加载时间：展示 top5 最慢
        2. 请求消耗时间：展示 top5 最慢
        3. 用户访问趋势：展示近 n 天的活动数量
    tags:
        - 用户
    parameters:
        - name: userID
          in: query
          type: string
          required: true
    """
    date_to = datetime.utcnow()  # The end date
    date_from = date_to - timedelta(days=7)  # The start date

    pageLoad_data = PageLoad.objects(
        user=ObjectId(userID)).order_by('-FCP').limit(5).scalar('FCP', 'pageUrl')
    request_data = RequestData.objects(user=ObjectId(
        userID)).order_by('-httpDuration').limit(5).scalar('httpDuration', 'targetURL')
    trend_data = list(
        RequestData
        .objects(user=ObjectId(userID))
        .filter(timestamp__gte=date_from, timestamp__lte=date_to)
        .aggregate([
            {
                '$group': {'_id': {"$dateToString": {'format': '%Y-%m-%d', 'date': '$timestamp'}}, 'count': {'$sum': 1}}
            }
        ])
    )
    trend_data.sort(key=(lambda x: x['_id']))
    # all_request = RequestData.objects(user=ObjectId(userID))
    # print(dir(trend_data))
    return successResponseWrap({
        'page': pageLoad_data,
        'request': request_data,
        'trend': trend_data,
        # 'all': all_request
    })
