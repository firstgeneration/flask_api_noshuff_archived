from flask_rest_jsonapi import ResourceList
from app import db
from .schemas import PostSchema
from app.models import Post
from ..decorators import login_required
from flask import g

class PostList(ResourceList):
    methods = ['POST']
    decorators = (login_required, )
    schema = PostSchema
    data_layer = {
        'session': db.session,
        'model': Post,
    }

    def create_object(self, data, kwargs):
        data['user'] = g.current_user.id
        super(PostList, self).create_object(data, kwargs)
