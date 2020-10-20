from app import db
from app.models import Post, Hashtag
from ..factories import UserFactory, HashtagFactory

def test_get_hashtags(client, make_headers):
    user = UserFactory()
    hashtags = HashtagFactory.create_batch(2)

    response = client.get(f'/api/v1/hashtags', headers=make_headers(user))
    
    assert response.status_code == 200
    hashtag_data = response.json['data']
    assert len(hashtag_data) == 2

def test_hashtag_create_from_post_caption(client, make_headers):
    user = UserFactory()
    data = {
        "data": {
            "type": "posts",
            "attributes": {
                "spotify_playlist_id": "test_spotify_playlist_id",
                "caption": "test_caption #tag1#tag2 #tag3 ##tag4 #tag4"
            }
        }
    }
    response = client.post('/api/v1/posts', json=data, headers=make_headers(user))

    assert response.status_code == 201
    assert Hashtag.query.count() == 4
