import pytest
from app import db
from ..factories import UserFactory

def test_unfollowed_posts(client):
    current_user, user2, user3, user4, user5 = UserFactory.create_batch(5, with_posts=2)
    current_user.following.append(user2)
    user2.following.append(current_user)
    user2.following.append(user3)
    user3.following.append(current_user)
    user3.following.append(user2)
    db.session.commit()

    results = current_user.unfollowed_posts()

    expected_post_ids = [5, 6, 7, 8, 9, 10]
    actual_post_ids = [p.id for p in results]
    actual_post_ids.sort()
    assert actual_post_ids == expected_post_ids
