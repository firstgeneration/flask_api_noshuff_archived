from app import db
from ..factories import UserFactory, PostFactory

def test_like_a_post(client):
    post = PostFactory()
    liker = UserFactory()

    post.likers.append(liker)
    db.session.commit()
    
    assert liker in post.likers

def test_ulike_a_post(client):
    post = PostFactory()
    liker = UserFactory()

    post.likers.append(liker)
    db.session.commit()
    assert liker in post.likers

    post.likers.remove(liker)
    db.session.commit()
    assert liker not in post.likers
