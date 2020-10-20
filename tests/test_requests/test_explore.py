from app import db
from ..factories import UserFactory

def test_get_explore(client, make_headers):
    current_user, followed_user, unfollowed_user = UserFactory.create_batch(3, with_posts=1)
    current_user.following.append(followed_user)
    wanted_post = unfollowed_user.posts[0]

    response = client.get(f'/api/v1/explore?include=user', headers=make_headers(current_user))

    assert response.status_code == 200

    post_data = response.json['data']
    assert len(post_data) == 1
    assert post_data[0]['id'] == str(wanted_post.id)
