from ..factories import CommentFactory

def test_post_comment(client, make_headers):
    parent_comment = CommentFactory(text='this is the parent comment')

    data = {
        "data": {
            "type": "comments",
            "attributes": {
                "text": "This is a child comment"
            },
            "relationships": {
                "post": {
                    "data": {
                        "type": "posts",
                        "id": parent_comment.post.id
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
    response = client.post('/api/v1/comments', json=data, headers=make_headers(parent_comment.author))

    assert response.status_code == 201

def test_get_comments_from_post(client, make_headers):
    comment = CommentFactory()

    response = client.get(
        '/api/v1/posts?include=comments.author',
        headers=make_headers(comment.author)
    )

    assert response.status_code == 200

def test_get_comments_from_all_posts(client, make_headers):
    parent_comment = CommentFactory(with_children=True)

    response = client.get('/api/v1/posts?include=comments.author&comments.children', headers=make_headers(parent_comment.author))

    assert response.status_code == 200

def test_get_child_comments_from_parent(client, make_headers):
    parent_comment = CommentFactory(with_children=True)

    response = client.get(
        f'/api/v1/comments/{parent_comment.id}?include=children.author',
        headers=make_headers(parent_comment.author)
    )

    assert response.status_code == 200
