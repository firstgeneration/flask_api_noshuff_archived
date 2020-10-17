from flask_rest_jsonapi import ResourceList, ResourceDetail, ResourceRelationship
from app import db
from .schemas import UserSchema, PostSchema
from app.models import User, Post
from ..decorators import login_required
from flask import g

class UserDetail(ResourceDetail):
    methods = ['GET']
    decorators = (login_required, )
    schema = UserSchema
    data_layer = {
        'session': db.session,
        'model': User,
    }

class UserRelationship(ResourceRelationship):
    decorators = (login_required, )
    schema = UserSchema
    data_layer = {
        'session': db.session,
        'model': User
    }

class PostList(ResourceList):
    methods = ['GET', 'POST']
    decorators = (login_required, )
    schema = PostSchema
    data_layer = {
        'session': db.session,
        'model': Post,
    }

    def create_object(self, data, kwargs):
        data['user'] = g.current_user.id
        super(PostList, self).create_object(data, kwargs)

class FeedList(ResourceList):
    def query(self, view_kwargs):
        return g.current_user.followed_posts()

    methods = ['GET']
    decorators = (login_required, )
    schema = PostSchema
    data_layer = {
        'session': db.session,
        'model': Post,
        'methods': {'query': query}
    }
