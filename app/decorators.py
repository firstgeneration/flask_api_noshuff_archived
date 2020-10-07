from functools import wraps
from flask import g, abort

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.current_user:
            abort(401, description="You must authenticate to perform this action")
        return f(*args, **kwargs)
    return decorated_function
