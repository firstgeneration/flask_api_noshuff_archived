from app import db
from app.models import User
from ..factories import UserFactory

def test_follow_user(client, make_headers):
    follower, followee = UserFactory.create_batch(2)
    assert followee not in follower.following

    data = {
        "data": [
            {
                "type": "users",
                "id": followee.id
            }
        ]
    }
    response = client.post(
        f'/api/v1/users/{follower.id}/relationships/follows',
        json=data, headers=make_headers(follower)
    )

    assert followee in follower.following

def test_unfollow_user(client, make_headers):
    follower, followee = UserFactory.create_batch(2)
    follower.following.append(followee)
    db.session.commit()
    assert followee in follower.following

    data = {
        "data": [
            {
                "type": "users",
                "id": followee.id
            }
        ]
    }
    response = client.delete(
        f'/api/v1/users/{follower.id}/relationships/follows',
        json=data, headers=make_headers(follower)
    )

    assert followee not in follower.following


def test_add_follow_for_another_user(client, make_headers):
    unknowing_follower, target_followee, malicious_user = UserFactory.create_batch(3)

    data = {
        "data": [
            {
                "type": "users",
                "id": target_followee.id
            }
        ]
    }
    response = client.post(
        f'/api/v1/users/{unknowing_follower.id}/relationships/follows',
        json=data, headers=make_headers(malicious_user)
    )

    assert response.status_code == 403
    assert target_followee not in unknowing_follower.following

def test_remove_follow_for_another_user(client, make_headers):
    unknowing_follower, target_followee, malicious_user = UserFactory.create_batch(3)
    unknowing_follower.following.append(target_followee)
    db.session.commit()
    assert target_followee in unknowing_follower.following

    data = {
        "data": [
            {
                "type": "users",
                "id": target_followee.id
            }
        ]
    }
    response = client.delete(
        f'/api/v1/users/{unknowing_follower.id}/relationships/follows',
        json=data, headers=make_headers(malicious_user)
    )

    assert response.status_code == 403
    assert target_followee in unknowing_follower.following
