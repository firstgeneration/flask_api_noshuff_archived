import factory
from app import models, db

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session = db.session

    spotify_id = 'test_spotify_id'
    email = 'test_email@noshuff.app'

class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Post
        sqlalchemy_session = db.session

    spotify_playlist_id = 'test_spotify_playlist_id'
    caption = "this is a test caption"
    user = factory.SubFactory(UserFactory)
