from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    profilePic = db.Column(db.String(100), default='tmpProfile.png')
    name = db.Column(db.String(100))
    userName = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    following = db.relationship('Follow', primaryjoin='User.userName == Follow.user')
    posts = db.relationship('Post', primaryjoin='User.userName == Post.userName')
    liked = db.relationship('Like')
    disLiked = db.relationship('DisLike')
    messages = db.relationship('Message', primaryjoin='User.id == Message.fromUserId')

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), ForeignKey('user.userName'))
    followedUser = db.Column(db.String(100), ForeignKey('user.userName'))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postDate = db.Column(db.String(20), default=datetime.today().strftime("%d/%m/%Y-%I:%M%p"))
    desc = db.Column(db.String(100))
    userName = db.Column(db.String(100), ForeignKey('user.userName'))
    userpic = db.Column(db.String(100), ForeignKey('user.profilePic'))
    likes = db.Column(db.Integer, default=0)
    disLikes = db.Column(db.Integer, default=0)
    liked = db.relationship('Like')
    disLiked = db.relationship('DisLike')

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, ForeignKey('post.id'))
    user = db.Column(db.String(100), ForeignKey('user.userName'))

class DisLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, ForeignKey('post.id'))
    user = db.Column(db.String(100), ForeignKey('user.userName'))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fromUserId = db.Column(db.Integer, ForeignKey('user.id'))
    toUserId = db.Column(db.Integer, ForeignKey('user.id'))
    msg = db.Column(db.String(100))
    date = db.Column(db.String(7), default=datetime.today().strftime("%d/%m/%Y-%I:%M%p"))