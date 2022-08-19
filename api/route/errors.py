from flask import Blueprint, jsonify, request, abort
from bson import ObjectId

from api.util.utils import failResponseWrap, successResponseWrap
from api.model.models import *
from ..util.data_process import get_errors_overview, get_error_detail_overview
from ..util.utils import get_past_days

api = Blueprint('errors', __name__, url_prefix='/error')


@api.route('/', methods=['GET'])
def get_errors():
    """返回所有Errors
    ---
    tags:
        - Errors
    parameters:
        - name: category
          in: query
          type: string
          required: false
        - name: userid
          in: query
          type: string
          required: false

    description:
        包含 error issue 所有信息的列表
        可以按照category或者user来查询
    """
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


@api.route('/issue/<errorID>', methods=['GET'])
def getErrorInfo(errorID):
    """查询某个 Error Issue
    ---
    tags:
        - Errors
    parameters:
        - name: errorID
          in: path
          type: string
          required: true
    """
    if not errorID:
        return failResponseWrap(msg='Error ID needed')
    
    try:
        errorIssue = ErrorData.objects(_id=ObjectId(errorID)).first()
        related_user = User.objects(_id=ObjectId(errorIssue['user']))

        if not errorIssue:
            return failResponseWrap(msg='Error not found')

        date_list = get_past_days(14)

        error_details = get_error_detail_overview(errorIssue['errorType'], errorIssue['originURL'], date_list)

        error_info = {
            'name': errorIssue['errorType'],
            'info': errorIssue,
            'details': error_details,
            'user': related_user
        }

        return successResponseWrap(error_info)

    except Exception as e:
        print(e)
        return failResponseWrap(msg='Internal Error')


@api.route('/issues/error-overview', methods=['GET'])
def error_overview():
    """返回过去30天Errors按照类别分类的统计信息
    ---
    tags:
        - Errors
    """
    date_list = get_past_days(30)
    data = get_errors_overview(date_list)

    return successResponseWrap({'dateList': date_list, 'data': data})


@api.route('/issues/list', methods=['GET'])
def error_list():
    """返回所有Errors信息并包含过去14天的统计信息(分页query可选)
    ---
    tags:
        - Errors
    parameters:
        - name: page
          in: query
          type: string
          required: false
        - name: items
          in: query
          type: string
          required: false
    """
    page_nb = request.args.get('page')
    items_per_page = request.args.get('items')

    error_issue_list = []
    date_list = get_past_days(14)

    if page_nb != None and items_per_page != None:
        offset = (int(page_nb)-1) * int(items_per_page)
        errors = ErrorData.objects.skip(offset).limit(int(items_per_page))
    else:
        errors = ErrorData.objects

    errors_count = ErrorData.objects.count()

    for error in errors:
        error_details = get_error_detail_overview(error['errorType'], error['originURL'], date_list)
        error_info = {
            'name': error['errorType'],
            'info': error,
            'details': error_details
        }
        error_issue_list.append(error_info)

    return successResponseWrap({'list': error_issue_list, 'dateList': date_list, 'total': errors_count})


