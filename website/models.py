from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    userName = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    posts = db.relationship('Post')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(100))
    userName = db.Column(db.String(100), ForeignKey('user.userName'))