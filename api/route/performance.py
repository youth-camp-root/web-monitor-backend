from flask import Blueprint, jsonify, request, abort
from bson import ObjectId

from api.util.utils import failResponseWrap, successResponseWrap
from api.model.models import *

api = Blueprint('performance', __name__, url_prefix='/performance')


@api.route('/', methods=["GET"])
def hello():
    return "Hello"
