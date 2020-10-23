from flask_rest_jsonapi import ResourceList, ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import JsonApiException, ObjectNotFound
from app import db
from .schemas import UserSchema, PostSchema, HashtagSchema, CommentSchema
from app.models import User, Post, Hashtag, Comment
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
    def after_create_object(self, obj, data, view_kwargs):
        if data.get('caption', None):
            Hashtag.save_from_string(data['caption'])

    methods = ['GET', 'POST']
    decorators = (login_required, )
    schema = PostSchema
    data_layer = {
        'session': db.session,
        'model': Post,
        'methods': {'after_create_object': after_create_object}
    }

    def create_object(self, data, kwargs):
        data['user'] = g.current_user.id
        super(PostList, self).create_object(data, kwargs)


class PostRelationship(ResourceRelationship):
    decorators = (login_required, )
    schema = PostSchema
    data_layer = {
        'session': db.session,
        'model': Post
    }


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


class CommentList(ResourceList):
    methods = ['GET', 'POST']
    decorators = (login_required, )
    schema = CommentSchema
    data_layer = {
        'session': db.session,
        'model': Comment
    }

    def create_object(self, data, view_kwargs):
        post = Post.query.filter_by(id=data['post']).first()
        if not post:
            raise ObjectNotFound(
                f'posts: {data["Post"]} not found',
                source={'parameter': 'post'}
            )

        parent = None
        if data.get('parent', None):
            parent = Comment.query.filter_by(id=data['parent']).first()
            if not parent:
                raise ObjectNotFound(
                    f'Comment: {data["parent"]} not found',
                    source={'parameter': 'parent'}
                )
        text = data['text']
        comment = Comment(post=post, parent=parent, author=g.current_user, text=text)

        db.session.add(comment)
        try:
            db.session.commit()
        except JsonApiException as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise JsonApiException("Object creation error: " + str(e), source={'pointer': '/data'})

        return comment
