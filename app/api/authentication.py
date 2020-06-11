from flask import g, jsonify, redirect, request
from ..models import User
from . import api
import requests

@api.route('/login', methods=['GET'])
def login():
    return {'test': 'test'}
#     spotify_token = request.args.get('spotify_token', '')
#     spotify_token_expires_in = request.args.get('spotify_token_expires_in', '')
    
#     spotify_user_data = get_spotify_user_data(spotify_token)
#     spotify_user_id = get_or_create_user(spotify_user_data.get('id'))
#     noshuff_access_token = generate_auth_token(spotify_user_id, spotify_token_expires_in)

#     return {
#         'spotify_access_token': spotify_access_token,
#         'noshuff_access_token': noshuff_access_token
#     })

# def get_spotify_user_data(spotify_access_token):
#     url = 'https://api.spotify.com/v1/me'
#     headers = { 'Authorization': f'Bearer {access_token}' }
#     response = requests.request('GET', url=url, headers=headers)
    
#     # handle case where spotify response fails
#     return  json.loads(response.content)

# # def get_or_create_user(spotify_user_id):
#     # check if user exists and if not create user
#     # generate JWT token
#     # send spotify data/token
