import requests
import json

def fetch_spotify_user_data(spotify_access_token):
    url = 'https://api.spotify.com/v1/me'
    headers = { 'Authorization': f'Bearer {spotify_access_token}' }
    response = requests.request('GET', url=url, headers=headers)
    # handle case where spotify response fails

    return json.loads(response.content)
