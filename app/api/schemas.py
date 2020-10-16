from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields

class UserSchema(Schema):
    class Meta:
        type_ = 'users'

    id = fields.Str(dump_only=True)
    display_name = fields.Str(dump_only=True)
    posts = Relationship(
        type_='posts',
        many=True,
        schema='PostSchema',
    )

class PostSchema(Schema):
    class Meta:
        type_ = 'posts'

    id = fields.Integer(as_string=True, dump_only=True)
    spotify_playlist_id = fields.Str(required=True)
    caption = fields.Str()
    user = Relationship(
        attribute='user',
        type_='users',
        schema='UserSchema',
    )
