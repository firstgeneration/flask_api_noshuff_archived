from .base import RequestTestBase
from unittest.mock import Mock, patch
from app import db
from app.models import User


class TestLogin(RequestTestBase):
    def setUp(self):
        super(TestLogin, self).setUp()
        self.user = User(spotify_id='test_spotify_id')
        db.session.add(self.user)
        db.session.commit()

    @patch('app.api.login.fetch_spotify_user_data')
    def test_login_existing_user(self, mock_spotify_fetch):
        mock_spotify_fetch.return_value = { 'id': 'test_spotify_id' }
        query_string = {
            'spotify_access_token': 'test_token',
            'spotify_access_token_expires_in': '360'
        }
        response = self.client.get('/api/v1/login', query_string=query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.query.count(), 1)

    @patch('app.api.login.fetch_spotify_user_data')
    def test_login_new_user(self, mock_spotify_fetch):
        mock_spotify_fetch.return_value = { 'id': 'test_spotify_id_new' }
        query_string = {
            'spotify_access_token': 'test_token',
            'spotify_access_token_expires_in': '360'
        }
        response = self.client.get('/api/v1/login', query_string=query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.query.count(), 2) 
