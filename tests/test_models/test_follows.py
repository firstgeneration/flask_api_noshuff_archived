import pytest
from app import db
from ..factories import UserFactory

def test_follow_user(client, make_headers):
    user1, user2 = UserFactory.create_batch(2)

    user1.following.append(user2)

    assert user2 in user1.following
    assert user1 in user2.followers
