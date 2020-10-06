from flask_rest_jsonapi import Api
from .resources import PostList

def register_resource_routes(app):
    api = Api(app)
    api.route(PostList, 'post_list', '/api/v1/posts')
