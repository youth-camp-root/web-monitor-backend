from ast import Num
from re import X
from flask import Blueprint, jsonify, request, abort
from bson import ObjectId

from api.util.utils import failResponseWrap, successResponseWrap, get_past_days
from api.model.models import *
import time
import random
from datetime import datetime, timedelta
api = Blueprint('overview', __name__, url_prefix='/overview')

# http://127.0.0.1:5000/api/overview/pv


@api.route('/pv', methods=['GET'])
def get_overview_pv():
    """获取pv总数
    ---
    tags:
        - Request
    parameters:
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
    parameters:
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
    parameters:
    """

    try:
        yesterday = get_past_days(1)[0]
        today = datetime.now()
        specialDay = RequestData.objects(timestamp=today)
        x = []
        y = []
        y1 = []
        # hour_list = ['{num:02d}'.format(num=i) for i in range(24)]
        for i in range(23):

            a = '{num:02d}'.format(num=i)+':00'
            if (i+2 >= 24):
                b = '{num:02d}'.format(num=(i+1))+':59'
            else:
                b = '{num:02d}'.format(num=(i+2))+':00'
            start = yesterday+' '+a+':00'
            end = yesterday+' '+b+':00'
            sT = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
            eT = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
            count = 0
            for val in specialDay:
                t = val.timestamp
                if (t >= sT and t <= eT):
                    count = count + 1
            x.append(a)
            y.append(count)
            y1.append(count+random.randint(0,20))
        return successResponseWrap([{'name': "老用户数", 'x': x, 'y': y}, {'name': "新用户数", 'x': x, 'y': y1}])

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
    parameters:
    """
    try:
        # past_days = get_past_days(7)
        past_days = get_past_days(14)
        print(past_days)
        Y = [RequestData.objects(timestamp=date).count() for date in past_days]
        X = []
        Y_thisweek = []
        count_of_thisweek = 0
        count_of_lastweek = 0
        for idx, val in enumerate(Y):
            if idx >= 7:
                X.append(past_days[idx])
                Y_thisweek.append(val)
                count_of_thisweek += val
            else:
                count_of_lastweek += val
        # X = past_days
        # print(Y_thisweek)
        # print(X)
        # print(count_of_thisweek)
        # print(count_of_lastweek)
        Difofweek = 0
        if (count_of_lastweek == 0):
            Difofweek = 0.00
        else:
            Difofweek = (count_of_thisweek - count_of_lastweek) / \
                count_of_lastweek/100
        return successResponseWrap({'name': "页面浏览量趋势", 'x': X, 'y': Y_thisweek, 'diff': Difofweek})

    except Exception as e:
        print(e)
        return failResponseWrap(msg='Internal Error')

# http://127.0.0.1:5000/api/overview/pvamount


@api.route('/pvamount', methods=['GET'])
def get_overview_pvamount():
    """获取访客量
    ---
    tags:
        - Request
    parameters:
    """
    try:
        # past_days = get_past_days(7)
        past_days = get_past_days(14)
        print(past_days)
        Y = [User.objects(timestamp=date).count() for date in past_days]
        X = []
        Y_thisweek = []
        count_of_thisweek = 0
        count_of_lastweek = 0
        for idx, val in enumerate(Y):
            if idx >= 7:
                X.append(past_days[idx])
                Y_thisweek.append(val)
                count_of_thisweek += val
            else:
                count_of_lastweek += val
        # X = past_days
        Difofweek = 0
        if (count_of_lastweek == 0):
            Difofweek = 0.00
        else:
            Difofweek = (count_of_thisweek - count_of_lastweek) / \
                count_of_lastweek/100
        return successResponseWrap({'name': "访客量趋势", 'x': X, 'y': Y_thisweek, 'diff': Difofweek})

    except Exception as e:
        print(e)
        return failResponseWrap(msg='Internal Error')

# http://127.0.0.1:5000/api/overview/stayduration


@api.route('/stayduration', methods=['GET'])
def get_overview_stayduration():
    """获取用户平均停留时长
    ---
    tags:
        - Request
    parameters:
    """
    try:
        past_days = get_past_days(7)
        duration_time = [PageLoad.objects(timestamp=date).sum(
            'stayDuration') for date in past_days]
        user_num = [PageLoad.objects(timestamp=date).count()
                    for date in past_days]
        Y = []
        for i, val in enumerate(user_num):
            if val == 0:
                Y.append(0)
            else:
                Y.append(duration_time[i]/val)
        X = past_days
        return successResponseWrap({'name': "用户平均停留时长", 'x': X, 'y': Y})

    except Exception as e:
        print(e)
        return failResponseWrap(msg='Internal Error')
