from flask import Blueprint, jsonify, request, abort
from bson import ObjectId
from api.util.utils import failResponseWrap, successResponseWrap
from api.model.models import *


api = Blueprint('sdk', __name__, url_prefix='/add')


@api.route('/user', methods=['GET'])
def add_user():
    data = {
        'device': request.args.get('device') if request.args.get('device') else '',
        'os': request.args.get('os') if request.args.get('os') else '',
        'browser': request.args.get('browser') if request.args.get('browser') else '',
        'ip': request.args.get('ip') if request.args.get('ip') else '',
        'tag': request.args.get('tag') if request.args.get('tag') else '',
        'page': request.args.get('page') if request.args.get('page') else ''
    }

    new_data = User(**data)
    new_data.save()
    return successResponseWrap(msg='data added')


@api.route('/pageload', methods=['GET'])
def add_pageload():
    data = {
        'user': request.args.get('user') if request.args.get('device') else 'user',
        'pageUrl': request.args.get('pageUrl') if request.args.get('pageUrl') else '',
        'timestamp': request.args.get('timestamp') if request.args.get('timestamp') else '',
        'FP': request.args.get('FP') if request.args.get('FP') else '',
        'FCP ': request.args.get('FCP ') if request.args.get('FCP ') else '',
        'DOMReady': request.args.get('DOMReady') if request.args.get('DOMReady') else '',
        'stayDuration': request.args.get('stayDuration') if request.args.get('stayDuration') else '',
    }
    new_data = PageLoad(**data)
    new_data.save()
    return successResponseWrap(msg='data added')


@api.route('/request', methods=['GET'])
def add_request():
    data = {
        'user': request.args.get('user') if request.args.get('device') else 'user',
        'targetURL': request.args.get('targetURL') if request.args.get('targetURL') else '',
        'statusCode': request.args.get('statusCode') if request.args.get('statusCode') else '',
        'timestamp': request.args.get('timestamp') if request.args.get('timestamp') else '',
        'eventType': request.args.get('eventType') if request.args.get('eventType') else '',
        'httpDuration': request.args.get('httpDuration') if request.args.get('httpDuration') else '',
        'dnsDuration': request.args.get('dnsDuration') if request.args.get('dnsDuration') else '',
        'params': request.args.get('params') if request.args.get('params') else '',
        'responseData': request.args.get('responseData') if request.args.get('responseData') else '',
        'is_error': request.args.get('is_error') if request.args.get('is_error') else False,
    }

    if request.args.get('is_error') == True:
        error_data = {
            'user': request.args.get('user') if request.args.get('device') else 'user',
            'category': 'Request',
            'originURL': request.args.get('originURL') if request.args.get('originURL') else '',
            'timestamp': request.args.get('timestamp') if request.args.get('timestamp') else '',
            'requestData': data
        }
        new_error = ErrorData(**error_data)
        new_error.save()

    new_data = RequestData(**data)
    new_data.save()
    return successResponseWrap(msg='data added')


@api.route('/error', methods=['GET'])
def add_error():
    data = {
        'user': request.args.get('user') if request.args.get('device') else 'user',
        'category': request.args.get('category') if request.args.get('category') else '',
        'originURL': request.args.get('originURL') if request.args.get('originURL') else '',
        'timestamp': request.args.get('timestamp') if request.args.get('timestamp') else '',
        'errorType': request.args.get('errorType') if request.args.get('errorType') else '',
        'errorMsg': request.args.get('errorMsg') if request.args.get('errorMsg') else '',
        'filename': request.args.get('filename') if request.args.get('filename') else '',
        'position': request.args.get('position') if request.args.get('position') else '',
        'stack': request.args.get('stack') if request.args.get('stack') else '',
        'selector': request.args.get('selector') if request.args.get('selector') else '',
        'tagName': request.args.get('tagName') if request.args.get('tagName') else '',
        'rsrcTimestamp': request.args.get('rsrcTimestamp') if request.args.get('rsrcTimestamp') else '',
        'emptyPoints': request.args.get('emptyPoints') if request.args.get('emptyPoints') else '',
        'screen': request.args.get('screen') if request.args.get('screen') else '',
        'viewPoint': request.args.get('viewPoint') if request.args.get('viewPoint') else '',
    }
    new_data = ErrorData(**data)
    new_data.save()
    return successResponseWrap(msg='data added')

