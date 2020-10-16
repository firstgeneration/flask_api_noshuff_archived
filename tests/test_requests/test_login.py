from app import db
from app.models import User
from ..factories import UserFactory

def spotify_user_response(user):
    return {
        'id': user.id,
        'email': user.email,
        'display_name': user.display_name
    }

def test_login_existing_user(client, mocker):
    user = UserFactory()
    mocker.patch('app.api.login.fetch_spotify_user_data', return_value=spotify_user_response(user))

    query_string = {
        'spotify_access_token': 'test_token',
        'spotify_access_token_expires_in': '360'
    }
    response = client.get('/api/v1/login', query_string=query_string)

    assert response.status_code == 200
    assert User.query.count() == 1

def test_login_existing_user_new_user_data(client, mocker):
    user = UserFactory()
    new_display_name = f'new_{user.display_name}'
    new_email = f'new_{user.email}'
    response_w_new_data = spotify_user_response(user)
    response_w_new_data['display_name'] = new_display_name
    response_w_new_data['email'] = new_email
    mocker.patch('app.api.login.fetch_spotify_user_data', return_value=response_w_new_data)

    query_string = {
        'spotify_access_token': 'test_token',
        'spotify_access_token_expires_in': '360'
    }
    response = client.get('/api/v1/login', query_string=query_string)

    assert response.status_code == 200
    assert User.query.count() == 1
    assert User.query.first().display_name == new_display_name
    assert User.query.first().email == new_email

def test_login_new_user(client, mocker):
    user = UserFactory.build()
    mocker.patch('app.api.login.fetch_spotify_user_data', return_value=spotify_user_response(user))

    query_string = {
        'spotify_access_token': 'test_token',
        'spotify_access_token_expires_in': '360'
    }
    response = client.get('/api/v1/login', query_string=query_string)

    assert response.status_code == 200
    assert User.query.count() == 1
