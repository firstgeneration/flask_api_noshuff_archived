from flask import current_app
from . import db
import jwt
import datetime

follows = db.Table('follows',
    db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow()),
    db.Column('follower_id', db.String, db.ForeignKey('users.id')),
    db.Column('followee_id', db.String, db.ForeignKey('users.id'))
)

class User(db.Model):
    __tablename__ = 'users'
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
    id = db.Column(db.String(64), primary_key=True)
    display_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True)
    posts = db.relationship('Post', backref='user', lazy=True)
    following = db.relationship(
        'User',
        secondary=follows,
        primaryjoin=follows.c.follower_id == id,
        secondaryjoin=follows.c.followee_id == id,
        backref='followers',
    )

    def followed_posts(self):
        return Post.query.join(
            follows,
            follows.c.followee_id == Post.user_id
        ).filter(
            follows.c.follower_id == self.id
        ).order_by(
            Post.created_at.desc()
        )

    @staticmethod
    def get_user_from_auth_token(token):
        decoded = User.decode_auth_token(token)
        id = decoded['id']
        user = User.query.filter_by(id=id).first()

        return user

    @staticmethod
    def decode_auth_token(token):
        # Add in error handling
        return jwt.decode(token, current_app.config['JWT_SECRET'], algorithms='HS256')

    def generate_auth_token(self, expires_in=360):
        return jwt.encode(
            {
                'id': self.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(expires_in)),
            },
            current_app.config['JWT_SECRET'],
            algorithm='HS256'
        )


class Post(db.Model):
    __tablename__ = 'posts'
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
    id = db.Column(db.Integer, primary_key=True)
    spotify_playlist_id = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    caption = db.Column(db.String(300))
