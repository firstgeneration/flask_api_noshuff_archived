from ..factories import UserFactory, PostFactory
from app import db
from app.models import Comment

def test_post_comment(client, make_headers):
    user = UserFactory()
    post = PostFactory()
    parent_comment = Comment(post=post, author=user, text='this is the parent comment')
    db.session.add(parent_comment)
    db.session.commit()

    data = {
        "data": {
            "type": "comments",
            "attributes": {
                "text": "This is a comment"
            },
            "relationships": {
                "post": {
                    "data": {
                        "type": "posts",
                        "id": post.id
                    }
                },
                "parent": {
                    "data": {
                        "type": "comments",
                        "id": parent_comment.id
                    }
                }
            }
        }
    }
    response = client.post('/api/v1/comments', json=data, headers=make_headers(user))

    assert response.status_code == 201
