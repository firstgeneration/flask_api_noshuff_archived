from flask import Blueprint
from flask_rest_jsonapi import Api
from .resources import UserDetail, UserList, PostList, UserRelationship, FeedList, HashtagList, ExploreList
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
api.route(UserList, 'user_list', '/api/v1/users')
api.route(PostList, 'post_list', '/api/v1/posts')
api.route(UserRelationship, 'user_follows', '/api/v1/users/<id>/relationships/follows')
api.route(FeedList, 'feed_list', '/api/v1/feed')
api.route(HashtagList, 'hashtag_list', '/api/v1/hashtags')
api.route(ExploreList, 'explore_list', '/api/v1/explore')
