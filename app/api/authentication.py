from flask import g, jsonify, redirect, request
from ..models import User
from . import api
import requests
import json
import jwt
import datetime
import os
from .. import db

@api.route('/login', methods=['GET'])
def login():
    spotify_access_token = request.args.get('spotify_access_token', '')
    spotify_access_token_expires_in = request.args.get('spotify_access_token_expires_in', '')
    
    spotify_user_data = get_spotify_user_data(spotify_access_token)
    noshuff_user = get_or_create_user(spotify_user_data.get('id'))
    noshuff_access_token = generate_access_token(noshuff_user.spotify_id, spotify_access_token_expires_in)

    return {
        'noshuff_access_token': noshuff_access_token.decode("utf-8")
    }

def get_spotify_user_data(spotify_access_token):
    url = 'https://api.spotify.com/v1/me'
    headers = { 'Authorization': f'Bearer {spotify_access_token}' }
    response = requests.request('GET', url=url, headers=headers)
    
    # handle case where spotify response fails

    return json.loads(response.content)

def get_or_create_user(spotify_id):
    user = User.query.filter_by(spotify_id=spotify_id).first()
    if not user:
        user = User(spotify_id=spotify_id)
        db.session.add(user)
        db.session.commit()

    return user

def generate_access_token(spotify_id, spotify_access_token_expires_in):
    noshuff_access_token = jwt.encode(
        {
            'spotify_id': spotify_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(spotify_access_token_expires_in)),
        },
        os.getenv('JWT_SECRET'),
        algorithm='HS256'
    )

    return noshuff_access_token
