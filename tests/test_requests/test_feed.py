from app import db
from ..factories import UserFactory

def test_get_feed(client, make_headers):
    current_user, followed_user = UserFactory.create_batch(2, with_posts=1)
    current_user.following.append(followed_user)
    unwanted_post = current_user.posts[0]
    wanted_post = followed_user.posts[0]

    response = client.get(f'/api/v1/feed?include=user', headers=make_headers(current_user))

    assert response.status_code == 200

    post_data = response.json['data']
    assert len(post_data) == 1
    assert post_data[0]['id'] == str(wanted_post.id)
