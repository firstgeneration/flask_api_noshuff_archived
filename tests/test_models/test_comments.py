from ..factories import CommentFactory

def test_create_comment_w_parent(client):
    comment = CommentFactory(with_parent=True)

    assert comment in comment.parent.children
