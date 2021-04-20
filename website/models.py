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
    comments = db.relationship('Comment')
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
    comments = db.Column(db.Integer, default=0)
    liked = db.relationship('Like')
    disLiked = db.relationship('DisLike')
    commented = db.relationship('Comment')

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, ForeignKey('post.id'))
    user = db.Column(db.String(100), ForeignKey('user.userName'))

class DisLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, ForeignKey('post.id'))
    user = db.Column(db.String(100), ForeignKey('user.userName'))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(100))
    postId = db.Column(db.Integer, ForeignKey('post.id'))
    userName = db.Column(db.String(50), ForeignKey('user.userName'))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fromUserId = db.Column(db.Integer, ForeignKey('user.id'))
    toUserId = db.Column(db.Integer, ForeignKey('user.id'))
    msg = db.Column(db.String(100))
    img = db.Column(db.String(100), default=None)
    date = db.Column(db.String(7), default=datetime.today().strftime("%d/%m/%Y-%I:%M%p"))