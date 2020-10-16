from flask import request
from app import db
from app.models import User
from . import authentication

from .spotify_utils import fetch_spotify_user_data

@authentication.route('/login', methods=['GET'])
def login():
    spotify_access_token = request.args.get('spotify_access_token', '')
    spotify_access_token_expires_in = request.args.get('spotify_access_token_expires_in', '')

    spotify_user_data = fetch_spotify_user_data(spotify_access_token)
    spotify_id = spotify_user_data.get('id')
    display_name = spotify_user_data.get('display_name')
    email = spotify_user_data.get('email')

    noshuff_user = User.query.filter_by(id=spotify_id).first()
    if not noshuff_user:
        noshuff_user = User(id=spotify_id, display_name=display_name, email=email)
        db.session.add(noshuff_user)
        db.session.commit()
    else:
        changed = False
        if noshuff_user.display_name != display_name:
            noshuff_user.display_name = display_name
            changed = True
        if noshuff_user.email != email:
            noshuff_user.email = email
            changed = True
        if changed:
            db.session.add(noshuff_user)
            db.session.commit()

    noshuff_access_token = noshuff_user.generate_auth_token(spotify_access_token_expires_in)

    return {
        'noshuff_access_token': noshuff_access_token.decode("utf-8")
    }
