from flask_rest_jsonapi import ResourceList
from app import db
from .schemas import PostSchema
from app.models import Post

class PostList(ResourceList):
    schema = PostSchema
    data_layer = {
        'session': db.session,
        'model': Post
    }
