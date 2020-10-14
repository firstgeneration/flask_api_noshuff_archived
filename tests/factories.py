import factory
from app import models, db

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    spotify_id = 'test_spotify_id'
    email = 'test_email@noshuff.app'

    @factory.post_generation
    def with_posts(obj, create, extracted, **kwargs):
        if extracted:
            PostFactory.create_batch(extracted, user=obj)


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Post
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    spotify_playlist_id = factory.Sequence(lambda n: f'test_spotify_playlist_id_{n}')
    caption = "this is a test caption"
    user = factory.SubFactory(UserFactory)
