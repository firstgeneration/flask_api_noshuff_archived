from . import resources
from flask import g
from flask import request
from flask_rest_jsonapi import JsonApiException
import ast

def permission_manager(view, view_args, view_kwargs, *args, **kwargs):
    if isinstance(view_args[0], resources.PostRelationship):
        if request.data:
            data = request.data.decode('utf-8')
            data = ast.literal_eval(data)
            for datum in data['data']:
                if datum['id'] != g.current_user.id:
                    raise JsonApiException(
                        'data/id',
                        "Cannot change likes for other users",
                        title='Permission denied',
                        status='403'
                    )
    elif isinstance(view_args[0], resources.UserRelationship):
        if view_kwargs['id'] != g.current_user.id:
            raise JsonApiException(
                'data/id',
                "Cannot change follows for other users",
                title='Permission denied',
                status='403'
            )
