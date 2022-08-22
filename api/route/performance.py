from statistics import mean
from flask import Blueprint, jsonify, request, abort
from bson import ObjectId

from api.util.utils import failResponseWrap, successResponseWrap
from api.model.models import *
from ..util.utils import get_past_days
from ..util.performance import get_page_detail_overview,get_api_detail_overview
import base64


api = Blueprint('performance', __name__, url_prefix='/performance')


@api.route('/page/overview', methods=['GET'])
def getPageOverview():
    date_list = get_past_days(7)
    chartData = []
    for name in ['FP', 'FCP', 'DOMReady', 'DNS']:
      dataArr = []
      for day in date_list:
          data = PageLoad.objects.filter(timestamp__gte=day + ' 00:00:00', timestamp__lte=day + ' 23:59:59').distinct(name)
          if data:
            data = mean(data)
          else:
            data = 0
          dataArr.append(data)
      chartData.append({
        'titleText': name,
        'contentData': dataArr,
        'xData': date_list
      })
    return successResponseWrap(chartData)

@api.route('/page/pagelist', methods=["GET"])
def getPageList():
    """获取所有的页面列表
    ---
    tags:
        - Performance
    """
    per_page_count = request.args.get('count')
    current_page = request.args.get('page')
    pages = PageLoad.objects.aggregate([
        {'$group': { "_id": "$pageUrl" }},
        {'$skip': (int(current_page) - 1) * int(per_page_count)},
        {'$limit': int(per_page_count)},
    ])
    # pages = PageLoad.objects.skip(int(per_page_count)*(int(current_page)-1)).limit(int(per_page_count))
    pagesCount = PageLoad.objects.count()

    pageUrlList = [page['_id'] for page in pages]
    
    date_list = get_past_days(7)

    if not pages:
        return failResponseWrap(msg='Page not found')
    else:
        return successResponseWrap({'pageUrlList': pageUrlList, 'pagesCount': pagesCount})

@api.route('/pageinfo/<pageUrl>', methods=["GET"])
def getPageInfo(pageUrl):
    """获取页面信息
    ---
    tags:
        - Performance
    """
    date_list = get_past_days(7)
    pageUrl = base64.b64decode(pageUrl.encode()).decode('utf-8')
    # return pageUrl
    page = get_page_detail_overview(pageUrl, date_list)
    if not page:
        return failResponseWrap(msg='Page not found')
    else:
        return successResponseWrap(page)

@api.route('/api/overview', methods=["GET"])
def getApiOverview():
    date_list = get_past_days(7)
    chartData = []
    dataArr = []
    dataArr2 = []
    for day in date_list:
        data = RequestData.objects.filter(timestamp__gte=day + ' 00:00:00', timestamp__lte=day + ' 23:59:59').distinct('httpDuration')
        if data:
            data = mean(data)
        else:
            data = 0
        dataArr.append(data)
        dataArr2.append(RequestData.objects.filter(timestamp__gte=day + ' 00:00:00', timestamp__lte=day + ' 23:59:59').count())
    chartData.append({
    'titleText': '平均请求耗时',
    'contentData': dataArr,
    'xData': date_list
    })
    chartData.append({
    'titleText': '总请求量',
    'contentData': dataArr2,
    'xData': date_list
    })
    return successResponseWrap(chartData)

@api.route('/api/apilist', methods=["GET"])
def getApiList():
    """获取所有的页面列表
    ---
    tags:
        - Performance
    """
    per_page_count = request.args.get('count')
    current_page = request.args.get('page')

    apis = RequestData.objects.filter(targetURL={"$regex": r"\/$"}).skip(int(per_page_count)*(int(current_page)-1)).limit(int(per_page_count))
    apisCount = RequestData.objects.count()

    apiList = [api['targetURL'] for api in apis]
    
    date_list = get_past_days(7)

    if not apis:
        return failResponseWrap(msg='Api not found')
    else:
        return successResponseWrap({'apiList': apiList, 'apisCount': apisCount})

@api.route('/apiinfo/<apiUrl>', methods=["GET"])
def getApiInfo(apiUrl):
    """获取页面信息
    ---
    tags:
        - Performance
    """
    date_list = get_past_days(7)
    apiUrl = base64.b64decode(apiUrl.encode()).decode('utf-8')
    # return pageUrl
    apiOverviewData = get_api_detail_overview(apiUrl, date_list)
    if not api:
        return failResponseWrap(msg='Api not found')
    else:
        return successResponseWrap(apiOverviewData)