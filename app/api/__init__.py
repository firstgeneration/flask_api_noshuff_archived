from flask import Blueprint
from flask_rest_jsonapi import Api
from .resources import UserDetail, PostList, UserRelationship
from ..decorators import authenticate_user

authentication = Blueprint('authentication', __name__)
from . import login

json_api = Blueprint('api', __name__)
@json_api.before_request
@authenticate_user
def before_request():
    """ Apply decorator to all endpoints. """
    pass

api = Api(blueprint=json_api)
api.route(UserDetail, 'user_detail', '/api/v1/users/<id>')
api.route(PostList, 'post_list', '/api/v1/posts')
api.route(UserRelationship, 'user_follows', '/api/v1/users/<id>/relationships/follows')
