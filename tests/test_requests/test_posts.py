from .base import RequestTestBase
from app import db
from app.models import User, Post


class TestPosts(RequestTestBase):
    def setUp(self):
        super(TestPosts, self).setUp()
        self.user = User(spotify_id='test_spotify_id')
        db.session.add(self.user)
        db.session.commit()
        token = self.user.generate_auth_token().decode('utf-8')
        self.headers = {
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
            'Authorization': f'Bearer {token}'
        }

    def test_post_post(self):
        data = {
            "data": {
                "type": "posts",
                "attributes": {
                    "spotify_playlist_id": "test_spotify_playlist_id",
                    "caption": "test_caption"
                }
            }
        }
        response = self.client.post('/api/v1/posts', json=data, headers=self.headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.query.count(), 1)
        post = Post.query.first()

        for attr, value in data["data"]["attributes"].items():
            self.assertEqual(getattr(post, attr), value)
        self.assertEqual(post.user.spotify_id, self.user.spotify_id)

    def test_post_post_wo_auth(self):
        data = {
            "data": {
                "type": "posts",
                "attributes": {
                    "spotify_playlist_id": "test_spotify_playlist_id"
                }
            }
        }
        del self.headers['Authorization']
        response = self.client.post('/api/v1/posts', json=data, headers=self.headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Post.query.count(), 0)

    def test_get_post(self):
        post = Post(spotify_playlist_id='test_spotify_playlist_id', user=self.user)
        db.session.add(post)
        db.session.commit()
        response = self.client.get('/api/v1/posts', headers=self.headers)

        self.assertEqual(response.status_code, 200)
