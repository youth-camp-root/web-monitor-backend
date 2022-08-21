import random
from flask import Blueprint
from api.util.utils import failResponseWrap, successResponseWrap, get_past_days
from api.model.models import *
from datetime import datetime, timedelta
api = Blueprint('overview', __name__, url_prefix='/overview')

# http://127.0.0.1:5000/api/overview/pv


@api.route('/pv', methods=['GET'])
def get_overview_pv():
    """获取pv总数
    ---
    tags:
        - Request
    """

    try:
        num = RequestData.objects.count()
        return successResponseWrap(num)

    except Exception as e:
        print(e)
        return failResponseWrap(msg='Internal Error')

# http://127.0.0.1:5000/api/overview/uv


@api.route('/uv', methods=['GET'])
def get_overview_uv():
    """获取uv总数
    ---
    tags:
        - Request
    """

    try:
        num = User.objects.count()
        return successResponseWrap(num)

    except Exception as e:
        print(e)
        return failResponseWrap(msg='Internal Error')

# http://127.0.0.1:5000/api/overview/useraction


@api.route('/useraction', methods=['GET'])
def get_overview_useraction():
    """获取用户量统计
    ---
    tags:
        - Request
    """
    now = datetime(2022, 8, 4, 0, 0, 0)

    pipeline = [
        {
            '$match': {
                'timestamp': {
                    '$gte': now - timedelta(days=1),
                    '$lte': now
                }
            }
        }, {
            '$group': {
                '_id': {
                    '$subtract': [
                        {
                            '$subtract': [
                                '$timestamp', datetime(
                                    1970, 1, 1, 0, 0, 0)
                            ]
                        }, {
                            '$mod': [
                                {
                                    '$subtract': [
                                        '$timestamp', datetime(
                                            1970, 1, 1, 0, 0, 0)
                                    ]
                                }, 7200000
                            ]
                        }
                    ]
                },
                'count': {
                    '$sum': 1
                }
            }
        }
    ]
    try:
        stat = list(PageLoad.objects().aggregate(pipeline))
        times = [(now - timedelta(hours=i*2)).strftime("%H:%M")
                 for i in range(12, 0, -1)]
        return successResponseWrap([
            {"name": "新用户数", 'x': times, 'y': [
                i['count'] for i in stat
            ]},
            {"name": "老用户数", 'x': times, 'y': [
                i['count'] + random.randint(0, 5) for i in stat]},
        ])

    except Exception as e:
        print(e)
        return failResponseWrap(msg='Internal Error')

# http://127.0.0.1:5000/api/overview/uvamount


@api.route('/uvamount', methods=['GET'])
def get_overview_uvamount():
    """获取页面浏览量
    ---
    tags:
        - Request
    """
    try:
        date_from = datetime(2022, 8, 10)
        date_to = datetime(2022, 8, 17)
        data = list(RequestData.objects().filter(timestamp__gte=date_from, timestamp__lte=date_to).aggregate([
            {
                '$group': {'_id': {"$dateToString": {'format': '%Y-%m-%d', 'date': '$timestamp'}}, 'count': {'$sum': 1}}
            }
        ]))
        X = [item['_id'] for item in data]
        Y = [item['count'] for item in data]
        return successResponseWrap({'name': "页面浏览量趋势", 'x': X, 'y': Y, 'diff': random.random()})

    except Exception as e:
        print(e)
        return failResponseWrap(msg='Internal Error')

# http://127.0.0.1:5000/api/overview/pvamount


@ api.route('/pvamount', methods=['GET'])
def get_overview_pvamount():
    """获取访客量
    ---
    tags:
        - Request
    """
    try:
        date_from = datetime(2022, 8, 10)
        date_to = datetime(2022, 8, 17)
        data = list(RequestData.objects().filter(timestamp__gte=date_from, timestamp__lte=date_to).aggregate([
            {
                '$group': {'_id': {"$dateToString": {'format': '%Y-%m-%d', 'date': '$timestamp'}}, 'count': {'$sum': 1}}
            }
        ]))
        X = [item['_id'] for item in data]
        Y = [item['count'] // 5 for item in data]
        return successResponseWrap({'name': "访客量趋势", 'x': X, 'y': Y, 'diff': random.random()})

    except Exception as e:
        print(e)
        return failResponseWrap(msg='Internal Error')

# http://127.0.0.1:5000/api/overview/stayduration


@ api.route('/stayduration', methods=['GET'])
def get_overview_stayduration():
    """获取用户平均停留时长
    ---
    tags:
        - Request
    """
    try:
        date_from = datetime(2022, 8, 10)
        date_to = datetime(2022, 8, 17)
        data = list(PageLoad.objects().filter(timestamp__gte=date_from, timestamp__lte=date_to).aggregate([
            {
                '$group': {'_id': {"$dateToString": {'format': '%Y-%m-%d', 'date': '$timestamp'}}, 'count': {'$avg': '$stayDuration'}}
            }
        ]))
        X = [item['_id'] for item in data]
        Y = [item['count'] // 5 for item in data]
        return successResponseWrap({'name': "用户平均停留时长", 'x': X, 'y': Y, 'diff': random.random()})

    except Exception as e:
        print(e)
        return failResponseWrap(msg='Internal Error')
