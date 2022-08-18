"""
mock_data_forger.py
- forge mocked data into database using command line tools

Created by Xiong Kaijie on 2022-08-01.
Contributed by: Xiong Kaijie
Copyright © 2022 team Root of ByteDance Youth Camp. All rights reserved.
"""

from flask import Blueprint
import click
import sys

from api.model.models import User, RequestData, ErrorData
from api.mock.data_generator import UserMaterial, RequestMaterial, ErrorMaterial
from api.util.data_process import merge_failed_request

cmd = Blueprint('cmd', __name__)


def str_to_class(classname):
    """Convert string variable to class object"""
    return getattr(sys.modules[__name__], classname)


def delete_collection(collection_name):
    if collection_name == 'all':
        for collection in ['User', 'RequestData', 'ErrorData']:
            str_to_class(collection).drop_collection()
        return 'Collection "user", "requestData", "errorData" dropped'
    else:
        try:
            str_to_class(collection_name).drop_collection()
            return 'Collection {} dropped'.format(collection_name)
        except AttributeError:
            return 'Collection {} not exists'.format(collection_name)


def user_forger(amount):
    """forge mock user data with specific amount

    Args:
        amount (Integer, default: 50 | Optional): the amount of user data to be generated

    Returns:
        bool: if forged successfully or not
    """
    try:
        if amount:
            users = UserMaterial().generate_user_data(int(amount))
        else:
            users = UserMaterial().generate_user_data()
        for user in users:
            new_user = User(**user)
            new_user.save()
        return True

    except ValueError:
        return False


def request_forger(amount):
    """forge mock request data with specific amount

    Args:
        amount (Integer | Optional): the amount of request data to be generated
        default: 30% of the amount of the current users

    Returns:
        bool: if forged successfully or not
    """
    try:
        current_user_amount = User.objects.count()

        if not amount:
            default_request_amount = int(current_user_amount*0.3)
            pipeline = [
                {'$sample': {'size': default_request_amount}}
            ]
            users = User.objects().aggregate(pipeline)

        elif int(amount) <= current_user_amount:
            pipeline = [
                {'$sample': {'size': int(amount)}}
            ]
            users = User.objects().aggregate(pipeline)

        else:
            return False

        reqs = RequestMaterial().generate_request_data(users)
        for req in reqs:
            new_req = RequestData(**req)
            new_req.save()
        return True

    except ValueError:
        return False


def error_forger(amount):
    """forge mock error data with specific amount

    Args:
        amount (Integer | Optional): the amount of error data to be generated
        default: 70% of the amount of the current users

    Returns:
        bool: if forged successfully or not
    """
    try:
        current_user_amount = User.objects.count()
        error_requests_amount = RequestData.objects(is_error=True).count()

        if not amount:
            default_error_amount = int(current_user_amount*0.7) - error_requests_amount
            pipeline = [
                {'$sample': {'size': default_error_amount}}
            ]
            users = User.objects().aggregate(pipeline)

        elif int(amount) <= current_user_amount:
            pipeline = [
                {'$sample': {'size': int(amount)-error_requests_amount}}
            ]
            users = User.objects().aggregate(pipeline)

        else:
            return False

        errs = ErrorMaterial().generate_error_data(users)
        for err in errs:
            new_err = ErrorData(**err)
            new_err.save()
        
        merge_failed_request(None)

        return True

    except ValueError:
        return False


@cmd.cli.command()
@click.argument('amount', required=False)
def forgeuser(amount):
    """default amount is 50"""
    if user_forger(amount):
        click.echo('Users data added')
    else:
        click.echo('Add users data failed')


@cmd.cli.command()
@click.argument('amount', required=False)
def forgerequest(amount):
    """default amount is 30% of user amount"""
    if request_forger(amount):
        click.echo('Request data added')
    else:
        click.echo('Add request data failed')


@cmd.cli.command()
@click.argument('amount', required=False)
def forgeerror(amount):
    """default amount is 70% of user amount"""
    if error_forger(amount):
        click.echo('Error data added')
    else:
        click.echo('Add error data failed')


@cmd.cli.command()
@click.argument('collection_name')
def drop(collection_name):
    """Drop the specified collection"""
    msg = delete_collection(collection_name)
    click.echo(msg)
