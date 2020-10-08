from werkzeug.wrappers import Request
from flask import g
from .models import User

class Middleware():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        response = Request(environ)
        auth_header = response.headers.get('Authorization', None)
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            if auth_token:
                # add error handling
                user = User.get_user_from_auth_token(auth_token)
                if user:
                    g.current_user = user
        else:
            g.current_user = None

        return self.app(environ, start_response)
