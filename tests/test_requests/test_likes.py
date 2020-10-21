from ..factories import UserFactory, PostFactory

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

    assert liker in post.likers

def test_unlike_post(client, make_headers):
    post = PostFactory(with_likers=1)
    liker = post.likers[0]

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

    assert liker not in post.likers
    assert len(post.likers) == 0
