from app import db
from app.models import Post
from ..factories import UserFactory, PostFactory

def test_post_post(client, make_headers):
    user = UserFactory()
    data = {
        "data": {
            "type": "posts",
            "attributes": {
                "spotify_playlist_id": "test_spotify_playlist_id",
                "caption": "test_caption"
            }
        }
    }
    response = client.post('/api/v1/posts', json=data, headers=make_headers(user))

    assert response.status_code == 201
    assert Post.query.count() == 1
    post = Post.query.first()
    assert post.user == user
    for attr, value in data["data"]["attributes"].items():
        assert getattr(post, attr) == value

def test_post_post_wo_auth(client, make_headers):
    user = UserFactory()
    data = {
        "data": {
            "type": "posts",
            "attributes": {
                "spotify_playlist_id": "test_spotify_playlist_id",
                "caption": "test_caption"
            }
        }
    }
    headers = make_headers(user)
    del headers['Authorization']
    response = client.post('/api/v1/posts', json=data, headers=headers)

    assert response.status_code == 401
    assert Post.query.count() == 0

def test_get_posts(client, make_headers):
    post = PostFactory()
    user = post.user
    response = client.get('/api/v1/posts?include=user', headers=make_headers(user))

    post_attrs = ['spotify_playlist_id', 'caption']
    # user_attrs = ['id']

    post_data = response.json['data']
    assert len(post_data) == 1
    user_data = response.json['included']
    assert len(user_data) == 1

    for attr in post_attrs:
        assert post_data[0]["attributes"][attr] == getattr(post, attr)
    # for attr in user_attrs:
    #     assert user_data[0]["attributes"][attr] == getattr(user, attr)

    assert response.status_code == 200
