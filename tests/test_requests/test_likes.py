from ..factories import UserFactory, PostFactory
from app import db

def test_like_post(client, make_headers):
    post = PostFactory()
    liker = UserFactory()

    data = {
        "data": [
            {
                "type": "users",
                "id": liker.id
            }
        ]
    }
    response = client.post(
        f'/api/v1/posts/{post.id}/relationships/likes',
        json=data, headers=make_headers(liker)
    )

    assert response.status_code == 200
    assert liker in post.likers

def test_unlike_post(client, make_headers):
    post = PostFactory(with_likers=1)
    liker = post.likers[0]
    assert liker in post.likers

    data = {
        "data": [
            {
                "type": "users",
                "id": liker.id
            }
        ]
    }
    response = client.delete(
        f'/api/v1/posts/{post.id}/relationships/likes',
        json=data, headers=make_headers(liker)
    )

    assert response.status_code == 200
    assert liker not in post.likers

def test_add_like_for_another_user(client, make_headers):
    post = PostFactory()
    unknowing_user, malicious_user = UserFactory.create_batch(2)

    data = {
        "data": [
            {
                "type": "users",
                "id": unknowing_user.id
            }
        ]
    }
    response = client.post(
        f'/api/v1/posts/{post.id}/relationships/likes',
        json=data, headers=make_headers(malicious_user)
    )

    assert response.status_code == 403
    assert len(post.likers) == 0

def test_remove_like_for_another_user(client, make_headers):
    post = PostFactory()
    unknowing_user, malicious_user = UserFactory.create_batch(2)
    post.likers.append(unknowing_user)
    db.session.commit()
    assert unknowing_user in post.likers

    data = {
        "data": [
            {
                "type": "users",
                "id": unknowing_user.id
            }
        ]
    }
    response = client.delete(
        f'/api/v1/posts/{post.id}/relationships/likes',
        json=data, headers=make_headers(malicious_user)
    )

    assert response.status_code == 403
    assert unknowing_user in post.likers
