from flask_rest_jsonapi import ResourceList, ResourceDetail, ResourceRelationship
from app import db
from .schemas import UserSchema, PostSchema, HashtagSchema
from app.models import User, Post, Hashtag
from ..decorators import login_required
from flask import g

class UserList(ResourceList):
    methods = ['GET']
    decorators = (login_required, )
    schema = UserSchema
    data_layer = {
        'session': db.session,
        'model': User
    }


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


class HashtagList(ResourceList):
    methods = ['GET']
    decorators = (login_required, )
    schema = HashtagSchema
    data_layer = {
        'session': db.session,
        'model': Hashtag
    }


class ExploreList(ResourceList):
    def query(self, view_kwargs):
        return g.current_user.unfollowed_posts()

    methods = ['GET']
    decorators = (login_required, )
    schema = PostSchema
    data_layer = {
        'session': db.session,
        'model': Post,
        'methods': {'query': query}
    }
