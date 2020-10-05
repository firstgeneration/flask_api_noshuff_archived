from flask import current_app
from . import db
import jwt
import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    posts = db.relationship('Post', backref='user', lazy=True)

#region

    # @staticmethod
    # def get_user_from_token(token):
    #     decoded = decode_access_token(token)
    #     spotify_id = decoded['spotify_id']
    #     user = User.query.filter(spotify_id=spotify_id).first()

    #     return user

    # @staticmethod
    # def decode_access_token(token):
    #     # Add in error handling
    #     return jwt.decode(token, current_app.config['JWT_SECRET'], algorithms='HS256')

    def generate_access_token(self, spotify_access_token_expires_in):
        return jwt.encode(
            {
                'spotify_id': self.spotify_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(spotify_access_token_expires_in)),
            },
            current_app.config['JWT_SECRET'],
            algorithm='HS256'
        )
#endregion
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    spotify_playlist_id = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
