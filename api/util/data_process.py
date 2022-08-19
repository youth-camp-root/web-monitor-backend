"""
data_process.py
- for data processing

Created by Xiong Kaijie on 2022-08-15.
Contributed by: Xiong Kaijie
Copyright © 2022 team Root of ByteDance Youth Camp. All rights reserved.
"""

from ..model.models import User, RequestData, ErrorData


def merge_failed_request(origin_url):
    req_pipeline = [
        {'$match': { 'is_error': True }},
    ]
    errorReqs = RequestData.objects().aggregate(req_pipeline)

    if errorReqs:
        for errorReq in errorReqs:
            error_info = {}
            error_info['category'] = 'Request'
            error_info['errorType'] = 'requestError'
            error_info['originURL'] = origin_url if origin_url else 'test.com/test'
            error_info['timestamp'] = errorReq['timestamp']
            error_info['requestData'] = errorReq
            new_error = ErrorData(**error_info)
            new_error.save()


def get_errors_overview(date_range):
    """Summarize error issues
    """
    error_overview_list = []

    error_all_overview = {
        'name': 'Total Error',
        'count': ErrorData.objects.count(),
        'value': [ErrorData.objects().filter(timestamp__gte=day + ' 00:00:00', timestamp__lte=day + ' 23:59:59').count() for day in date_range]
    }

    error_overview_list.append(error_all_overview)
    
    for item in ['JS', 'Request', 'Resource', 'BlankScreen']:
        error_type_overview = {}
        if item == 'JS':
            error_type_overview['name'] = 'JS Error'
            error_type_overview['count'] = ErrorData.objects(category='JS').count() + ErrorData.objects(category='Promise').count()
            error_type_overview['value'] = [ErrorData.objects(category='JS').filter(timestamp__gte=day + ' 00:00:00', timestamp__lte=day + ' 23:59:59').count() + ErrorData.objects(category='Promise').filter(timestamp__gte=day + ' 00:00:00', timestamp__lte=day + ' 23:59:59').count() for day in date_range]
        elif item == 'Request':
            error_type_overview['name'] = 'API Error'
            error_type_overview['count'] = ErrorData.objects(category='Request').count()
            error_type_overview['value'] = [ErrorData.objects(category='Request').filter(timestamp__gte=day + ' 00:00:00', timestamp__lte=day + ' 23:59:59').count() for day in date_range]
        elif item == 'Resource':
            error_type_overview['name'] = 'Resource Error'
            error_type_overview['count'] = ErrorData.objects(category='Resource').count()
            error_type_overview['value'] = [ErrorData.objects(category='Resource').filter(timestamp__gte=day + ' 00:00:00', timestamp__lte=day + ' 23:59:59').count() for day in date_range]
        elif item == 'BlankScreen':
            error_type_overview['name'] = 'BlankScreen Error'
            error_type_overview['count'] = ErrorData.objects(category='BlankScreen').count()
            error_type_overview['value'] = [ErrorData.objects(category='BlankScreen').filter(timestamp__gte=day + ' 00:00:00', timestamp__lte=day + ' 23:59:59').count() for day in date_range]
        error_overview_list.append(error_type_overview)

    return error_overview_list


def get_error_detail_overview(error_type, origin_url, date_range):
    """Count total, affected users and occurances of an error within last 14 days
    """

    error_freq = [ErrorData.objects(errorType=error_type, originURL=origin_url).filter(timestamp__gte=day + ' 00:00:00', timestamp__lte=day + ' 23:59:59').count() for day in date_range]

    total_error_cnt = ErrorData.objects(errorType=error_type, originURL=origin_url).count()

    user_affected_cnt = len(ErrorData.objects(errorType=error_type, originURL=origin_url).distinct('user'))

    return {
        'errorFreq': error_freq ,
        'TotalErrCnt': total_error_cnt,
        'userAffectCnt': user_affected_cnt
    }

