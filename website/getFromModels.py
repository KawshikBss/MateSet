from .models import User, Post
from . import db

def get_users_following(user):
    nameUsersFollowing = get_users_following_name(user)
    users = User.query.all()
    return [usr for usr in users if usr.userName in nameUsersFollowing]

def get_users_following_name(user):
    return [usr.followedUser for usr in user.following]

def get_users_suggestions(user):
    usersFollowing = get_users_following_name(user)
    return [sug for sug in User.query.all() if not sug.id == user.id and sug.userName not in usersFollowing]

def get_posts_for_user(user):
    usersFollowing = get_users_following_name(user)
    posts = Post.query.all()
    return [post for post in posts if post.userName in usersFollowing or post.userName == user.userName]