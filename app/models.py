from flask import current_app
from . import db
import jwt
import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(64), primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    posts = db.relationship('Post', backref='user', lazy=True)

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
    id = db.Column(db.Integer, primary_key=True)
    spotify_playlist_id = db.Column(db.String(64))
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    caption = db.Column(db.String(300))
