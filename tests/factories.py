import factory
from app import models, db

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: f'test_spotify_id{n+1}')
    display_name = factory.Sequence(lambda n: f'test_spotify_display_name{n+1}')
    email = factory.Sequence(lambda n: f'test_email@noshuff.app{n+1}')

    @factory.post_generation
    def with_posts(obj, create, extracted, **kwargs):
        if extracted:
            PostFactory.create_batch(extracted, user=obj)


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Post
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    spotify_playlist_id = factory.Sequence(lambda n: f'test_spotify_playlist_id_{n+1}')
    caption = factory.Sequence(lambda n: f'this is a test caption{n+1}')
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def with_likers(obj, create, extracted, **kwargs):
        if extracted:
            users = UserFactory.create_batch(extracted)
            for user in users:
                obj.likers.append(user)
            db.session.commit()

class HashtagFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Hashtag
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    tag = factory.Sequence(lambda n: f'tag{n+1}')

class CommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Comment
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    text = factory.Sequence(lambda n: f'this is a comment{n+1}')
    author = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)

    class Params:
        with_parent = factory.Trait(
            parent = factory.SubFactory('tests.factories.CommentFactory', post=factory.SelfAttribute('..post'))
        )

    @factory.post_generation
    def with_children(obj, create, extracted, **kwargs):
        if extracted:
            children = CommentFactory(parent=obj, post=obj.post)
