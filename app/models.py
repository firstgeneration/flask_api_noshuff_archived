from flask import current_app
from . import db
import jwt
import datetime
import re
from sqlalchemy_utils import LtreeType, Ltree

follows = db.Table('follows',
    db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow),
    db.Column('follower_id', db.String, db.ForeignKey('users.id')),
    db.Column('followee_id', db.String, db.ForeignKey('users.id'))
)

likes = db.Table('likes',
    db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('user_id', db.String, db.ForeignKey('users.id'))
)

class User(db.Model):
    __tablename__ = 'users'
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    id = db.Column(db.String(64), primary_key=True)
    display_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True)
    avatar_url = db.Column(db.String(500))
    posts = db.relationship('Post', backref='user', lazy=True)
    following = db.relationship(
        'User',
        secondary=follows,
        primaryjoin=follows.c.follower_id == id,
        secondaryjoin=follows.c.followee_id == id,
        backref='followers',
    )
    comments = db.relationship('Comment', backref='author', lazy=True)

    def followed_posts(self):
        return Post.query \
            .join(
                follows,
                follows.c.followee_id == Post.user_id) \
            .filter(follows.c.follower_id == self.id) \
            .order_by(Post.created_at.desc())

    def unfollowed_posts(self):
        return Post.query \
            .outerjoin(
                follows,
                db.and_(follows.c.followee_id == Post.user_id, \
                        follows.c.follower_id == self.id)) \
            .filter(follows.c.followee_id == None) \
            .filter(Post.user_id != self.id) \
            .order_by(Post.created_at.desc())

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
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    spotify_playlist_id = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    caption = db.Column(db.String(300))
    likers = db.relationship('User', secondary="likes")
    comments = db.relationship('Comment', backref='post', lazy=True)


class Hashtag(db.Model):
    __tablename__ = 'hashtags'
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64), unique=True, nullable=False)

    @staticmethod
    def save_from_string(string):
        regex = re.compile(r'#\w+')
        for tag in re.findall(regex, string):
            clean_tag = tag[1:].lower()
            if (len(clean_tag) <= 64) and not Hashtag.query.filter_by(tag=clean_tag).first():
                db.session.add(Hashtag(tag=clean_tag))
                db.session.commit()


id_seq = db.Sequence('comments_id_seq')
class Comment(db.Model):
    __tablename__ = 'comments'
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    path = db.Column(LtreeType, nullable=False)
    parent = db.relationship(
        'Comment',
        primaryjoin=db.remote(path) == db.foreign(db.func.subpath(path, 0, -1)),
        backref='children',
        sync_backref=False,
        viewonly=True
    )

    def __init__(self, post, author, text, parent=None):
        _id = db.engine.execute(id_seq)
        self.id = _id
        self.post = post
        self.author = author
        self.text = text
        ltree_id = Ltree(str(_id))
        self.path = ltree_id if parent is None else parent.path + ltree_id

    __table_args__ = (db.Index('ix_comments_path', path, postgresql_using='gist'),)
