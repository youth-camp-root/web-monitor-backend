"""
api.py
"""

from flask import Blueprint, jsonify, request, abort
from bson.objectid import ObjectId

from api.util.utils import failResponseWrap, successResponseWrap
from api.model.models import *
from api.route.user import api as user_api
from api.route.mock_api import api as mock_api
from api.route.performance import api as performance_api
from ..util.data_process import get_errors_overview, get_error_detail_overview, get_past_days

api = Blueprint('api', __name__, url_prefix='/api')
api.register_blueprint(user_api)
api.register_blueprint(mock_api)
api.register_blueprint(performance_api)


@api.route('/request', methods=['GET'])
def get_request():
    reqs = RequestData.objects
    return successResponseWrap(reqs)


@api.route('/errors', methods=['GET'])
def get_errors():
    category = request.args.get('category')
    userID = request.args.get('userid')

    if category:
        errors = ErrorData.objects(category=category)
    elif userID:
        errors = ErrorData.objects(user=ObjectId(userID))
    else:
        errors = ErrorData.objects

    if not errors:
        return failResponseWrap(msg='Error not found')
    else:
        return successResponseWrap(errors)


@api.route('/error/issue', methods=['GET'])
def getErrorInfo():
    error_id = request.args.get('id')

    if not error_id:
        return failResponseWrap(msg='Error ID needed')
    
    try:
        errorIssue = ErrorData.objects(_id=ObjectId(error_id)).first()

        if not errorIssue:
            return failResponseWrap(msg='Error not found')

        error_details = get_error_detail_overview(errorIssue['errorType'], errorIssue['originURL'])

        error_info = {
            'name': errorIssue['errorType'],
            'info': errorIssue,
            'details': error_details
        }

        return successResponseWrap(error_info)

    except Exception as e:
        print(e)
        return failResponseWrap(msg='Internal Error')


# ----------------------------------------- Statistics -------------------------------------

@api.route('/error/issues/error-overview', methods=['GET'])
def error_overview():
    data = get_errors_overview()
    date_list = get_past_days(30)

    return successResponseWrap({'dateList': date_list, 'data': data})


@api.route('/error/issues/list', methods=['GET'])
def error_list():

    error_issue_list = []

    date_list = get_past_days(30)
    errors = ErrorData.objects
    errors_count = ErrorData.objects.count()

    for error in errors:
        error_details = get_error_detail_overview(error['errorType'], error['originURL'])
        error_info = {
            'name': error['errorType'],
            'info': error,
            'details': error_details
        }
        error_issue_list.append(error_info)

    return successResponseWrap({'list': error_issue_list, 'dateList': date_list, 'total': errors_count})

