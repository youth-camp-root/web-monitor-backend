from ..model.models import User, RequestData, ErrorData, PageLoad
from bson import ObjectId
from statistics import *

def get_page_detail_overview(pageUrl, date_range):
    pages = PageLoad.objects.filter(pageUrl=pageUrl, timestamp__gte=date_range[0] + ' 00:00:00', timestamp__lte=date_range[len(date_range)-1] + ' 23:59:59')

    webVitail = [
        {
          'name': 'good',
          'value': pages.filter(DOMReady__lte=100.0).count()
        },{
          'name': 'medium',
          'value': pages.filter(DOMReady__gte=100.0).filter(DOMReady__lt=300.0).count()
        },{
          'name': 'bad',
          'value': pages.filter(DOMReady__gte=300.0).count()
        }
      ]
    
    

    chartData = []
    for name in ['DOMReady', 'stayDuration']:
      dataArr = []
      for day in date_range:
          data = PageLoad.objects.filter(pageUrl=pageUrl, timestamp__gte=day + ' 00:00:00', timestamp__lte=day + ' 23:59:59').distinct(name)
          if data:
            data = mean(data)
          else:
            data = 0
          dataArr.append(data)
      chartData.append({
        'titleText': name,
        'contentData': dataArr,
        'xData': date_range
      })

    tagsData = []
    tagsData = pages.distinct('user')

    errorsData = []
    errorsData = ErrorData.objects.filter(originURL=pageUrl, timestamp__gte=date_range[0] + ' 00:00:00', timestamp__lte=date_range[len(date_range)-1] + ' 23:59:59').count()

    return {
      'webVitals': webVitail,
      'chartData': chartData,
      'tagsData': tagsData,
      'errorCount': errorsData
    }
  
def get_api_detail_overview(apiUrl, date_range):
    apis = RequestData.objects.filter(targetURL=apiUrl, timestamp__gte=date_range[0] + ' 00:00:00', timestamp__lte=date_range[len(date_range)-1] + ' 23:59:59')

    dataArr = []
    for day in date_range:
        data = RequestData.objects.filter(targetURL=apiUrl, timestamp__gte=day + ' 00:00:00', timestamp__lte=day + ' 23:59:59').count()
        dataArr.append(data)

    return {
      'apiVitals': [{
        'name': 'good',
        'value': apis.filter(httpDuration__lte=3000.0).count()
      },{
        'name': 'medium',
        'value': apis.filter(httpDuration__gte=3000.0).filter(httpDuration__lt=7000.0).count()
      },{
        'name': 'bad',
        'value': apis.filter(httpDuration__gte=7000.0).count()
      }],
      'chartData': {
        'titleText': '访问量',
        'contentData': dataArr,
        'xData': date_range
      }
    }
    
