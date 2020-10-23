from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields
from flask import g

class UserSchema(Schema):
    class Meta:
        type_ = 'users'

    id = fields.Str(dump_only=True)
    display_name = fields.Str(dump_only=True)
    is_following = fields.Function(lambda obj: obj in g.current_user.following)
    posts = Relationship(
        type_='posts',
        many=True,
        schema='PostSchema',
    )
    follows = Relationship(
        attribute='following',
        many=True,
        schema='UserSchema',
        type_='users'
    )


class PostSchema(Schema):
    class Meta:
        type_ = 'posts'

    id = fields.Integer(as_string=True, dump_only=True)
    spotify_playlist_id = fields.Str(required=True)
    caption = fields.Str()
    is_liked = fields.Function(lambda obj: g.current_user in obj.likers)
    likes_count = fields.Function(lambda obj: len(obj.likers))
    user = Relationship(
        attribute='user',
        type_='users',
        schema='UserSchema',
    )
    likes = Relationship(
        attribute='likers',
        many=True,
        schema='UserSchema',
        type_='users'
    )


class HashtagSchema(Schema):
    class Meta:
        type_ = 'hashtags'

    id = fields.Integer(as_string=True, dump_only=True)
    tag = fields.Str()


class CommentSchema(Schema):
    class Meta:
        type_ = 'comments'

    id = fields.Integer(as_string=True, dump_only=True)
    text = fields.Str(required=True)
    author = Relationship(
        attribute='author',
        type_='users',
        schema='UserSchema',
    )
    post = Relationship(
        required=True,
        attribute='post',
        schema='PostSchema',
        type_='posts'
    )
    parent = Relationship(
        attribute='parent',
        schema='CommentSchema',
        type_='comments'
    )
