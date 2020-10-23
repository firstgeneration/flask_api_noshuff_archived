from flask import Blueprint
from flask_rest_jsonapi import Api
from . import resources
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
api.route(resources.UserDetail, 'user_detail', '/api/v1/users/<id>')
api.route(resources.UserList, 'user_list', '/api/v1/users')
api.route(resources.PostList, 'post_list', '/api/v1/posts')
api.route(resources.UserRelationship, 'user_follows', '/api/v1/users/<id>/relationships/follows')
api.route(resources.FeedList, 'feed_list', '/api/v1/feed')
api.route(resources.HashtagList, 'hashtag_list', '/api/v1/hashtags')
api.route(resources.ExploreList, 'explore_list', '/api/v1/explore')
api.route(resources.PostRelationship, 'post_likes', '/api/v1/posts/<int:id>/relationships/likes')
api.route(resources.CommentList, 'comment_list', '/api/v1/comments')
