from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields

class PostSchema(Schema):
    class Meta:
        type_ = 'posts'

    id = fields.Integer(as_string=True, dump_only=True)
    spotify_playlist_id = fields.Str(required=True)
    caption = fields.Str()
    user = Relationship(
        type_='users'
    )
