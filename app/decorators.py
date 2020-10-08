from functools import wraps
from flask import request, g, abort, make_response, jsonify
from .models import User

def authenticate_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            if auth_token:
                # add error handling
                user = User.get_user_from_auth_token(auth_token)
                if user:
                    g.current_user = user
        else:
            g.current_user = None
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.current_user:
            # Improve JSON format for jsonapi spec
            abort(make_response(jsonify(message="You must authenticate to perform this action"), 401))
        return f(*args, **kwargs)
    return decorated_function
