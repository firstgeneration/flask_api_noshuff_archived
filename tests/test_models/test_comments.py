from ..factories import PostFactory, UserFactory
from app.models import Comment
from app import db

def test_create_comment(client):
    post = PostFactory()
    commenter = UserFactory()
    parent_comment = Comment(post=post, author=commenter, text="This is my comment")
    db.session.add(parent_comment)
    db.session.commit()

    child_comment = Comment(parent=parent_comment, post=post, author=commenter, text="This is my comment")
    db.session.add(parent_comment)
    db.session.commit()

    assert child_comment in parent_comment.children
    assert parent_comment == child_comment.parent
