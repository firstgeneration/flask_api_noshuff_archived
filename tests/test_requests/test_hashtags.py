from app import db
from app.models import Post
from ..factories import UserFactory, HashtagFactory

def test_get_hashtags(client, make_headers):
    user = UserFactory()
    hashtags = HashtagFactory.create_batch(2)

    response = client.get(f'/api/v1/hashtags', headers=make_headers(user))
    
    assert response.status_code == 200
    hashtag_data = response.json['data']
    assert len(hashtag_data) == 2
