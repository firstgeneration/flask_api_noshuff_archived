from .base import RequestTestBase
from app import db
from app.models import User, Post


class TestPosts(RequestTestBase):
    def setUp(self):
        super(TestPosts, self).setUp()
        self.headers = {
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json"
        }
        self.user = User(spotify_id='test_spotify_id')
        db.session.add(self.user)
        db.session.commit()

    def test_users_get(self):
        data = {
            "data": {
                "type": "posts",
                "attributes": {
                    "spotify_playlist_id": "test_spotify_playlist_id"
                },
                "relationships": {
                    "user": {
                        "data": {
                            "type": "users",
                            "id": self.user.id
                        }
                    }
                }
            }
        }

        response = self.client.post('/api/v1/posts', json=data, headers=self.headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.query.count(), 1)
        self.assertEqual(Post.query.first().user.spotify_id, self.user.spotify_id)
