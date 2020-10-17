from app import db
from app.models import User
from ..factories import UserFactory

def test_follow_user(client, make_headers):
    user1, user2 = UserFactory.create_batch(2)
    assert user2 not in user1.following

    data = {
        "data": [
            {
                "type": "users",
                "id": user2.id
            }
        ]
    }
    response = client.post(
        f'/api/v1/users/{user1.id}/relationships/follows',
        json=data, headers=make_headers(user1)
    )

    assert user2 in user1.following

def test_unfollow_user(client, make_headers):
    user1, user2 = UserFactory.create_batch(2)
    user1.following.append(user2)
    db.session.commit()
    assert user2 in user1.following

    data = {
        "data": [
            {
                "type": "users",
                "id": user2.id
            }
        ]
    }
    response = client.delete(
        f'/api/v1/users/{user1.id}/relationships/follows',
        json=data, headers=make_headers(user1)
    )

    assert user2 not in user1.following
