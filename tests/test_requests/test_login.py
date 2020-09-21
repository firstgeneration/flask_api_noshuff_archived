import unittest
from unittest.mock import Mock, patch
from flask import current_app
from app import create_app, db
from app.models import User

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(spotify_id='test_spotify_id')
        db.session.add(self.user)
        db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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
