from app import db
from app.models import User

def test_login_existing_user(client, mocker):
    mocker.patch('app.api.login.fetch_spotify_user_data', return_value={ 'id': 'test_spotify_id' })

    user = User(spotify_id='test_spotify_id')
    db.session.add(user)
    db.session.commit()
    query_string = {
        'spotify_access_token': 'test_token',
        'spotify_access_token_expires_in': '360'
    }
    response = client.get('/api/v1/login', query_string=query_string)

    assert response.status_code == 200
    assert User.query.count() == 1

def test_login_new_user(client, mocker):
    mocker.patch('app.api.login.fetch_spotify_user_data', return_value={ 'id': 'test_spotify_id_new' })

    query_string = {
        'spotify_access_token': 'test_token',
        'spotify_access_token_expires_in': '360'
    }
    response = client.get('/api/v1/login', query_string=query_string)

    assert response.status_code == 200
    assert User.query.count() == 1
