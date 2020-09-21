from flask import request
from ..models import User
from . import api
import jwt
from .. import db
from .spotify_utils import fetch_spotify_user_data

@api.route('/login', methods=['GET'])
def login():
    spotify_access_token = request.args.get('spotify_access_token', '')
    spotify_access_token_expires_in = request.args.get('spotify_access_token_expires_in', '')

    spotify_user_data = fetch_spotify_user_data(spotify_access_token)
    spotify_id = spotify_user_data.get('id')

    noshuff_user = User.query.filter_by(spotify_id=spotify_id).first()
    if not noshuff_user:
        noshuff_user = User(spotify_id=spotify_id)
        db.session.add(noshuff_user)
        db.session.commit()

    noshuff_access_token = noshuff_user.generate_access_token(spotify_access_token_expires_in)

    return {
        'noshuff_access_token': noshuff_access_token.decode("utf-8")
    }
