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
    email = spotify_user_data.get('email')
    display_name = spotify_user_data.get('display_name')
    try:
        avatar_url = spotify_user_data['images'][0]['url']
    except:
        avatar_url = ''

    noshuff_user = User.query.filter_by(id=spotify_id).first()
    if not noshuff_user:
        noshuff_user = User(
            id=spotify_id,
            display_name=display_name,
            email=email,
            avatar_url=avatar_url
        )
        db.session.add(noshuff_user)
        db.session.commit()
    else:
        changed = False
        attrs = {
            'display_name': display_name,
            'email': email,
            'avatar_url': avatar_url,
        }

        for attr, val in attrs.items():
            if getattr(noshuff_user, attr) != val:
                setattr(noshuff_user, attr, val)
                changed = True
        if changed:
            db.session.add(noshuff_user)
            db.session.commit()

    noshuff_access_token = noshuff_user.generate_auth_token(spotify_access_token_expires_in)

    return {
        'noshuff_access_token': noshuff_access_token.decode("utf-8"),
        'user_id': noshuff_user.id,
        'display_name': noshuff_user.display_name,
        'avatar_url': noshuff_user.avatar_url,
    }
