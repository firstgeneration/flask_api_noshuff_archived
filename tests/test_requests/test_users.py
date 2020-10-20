from app import db
from app.models import Post
from ..factories import UserFactory

def test_get_user_w_posts(client, make_headers):
    user = UserFactory(with_posts=1)
    response = client.get(f'/api/v1/users/{user.id}?include=posts', headers=make_headers(user))

    # user_attrs = ['id']
    post_attrs = ['spotify_playlist_id', 'caption']
    user_data = response.json['data']
    post_data = response.json['included']
    assert len(post_data) == 1

    # for attr in user_attrs:
    #     assert user_data["attributes"][attr] == getattr(user, attr)
    for attr in post_attrs:
        assert post_data[0]["attributes"][attr] == getattr(user.posts[0], attr)
    
    assert response.status_code == 200

def test_patch_user(client, make_headers):
    user = UserFactory()
    data = {
        "data": {
            "type": "users",
            "id": user.id,
            "attributes": {
                "spotify_id": "different_test_spotify_playlist_id",
            }
        }
    }
    response = client.patch(f'/api/v1/users/{user.id}', headers=make_headers(user))

    assert response.status_code == 405

def test_get_users(client, make_headers):
    users = UserFactory.create_batch(2)

    response = client.get(f'/api/v1/users', headers=make_headers(users[0]))

    assert response.status_code == 200
    user_data = response.json['data']
    assert len(user_data) == 2
