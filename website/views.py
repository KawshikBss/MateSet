from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory
from flask_login import login_required, current_user
from .models import User, Post, Message
from . import db
from .getFromModels import *
#from file import send_image

# defining blueprint
views = Blueprint("views", __name__)

# defining route to homepage
@views.route('/', methods=['GET', 'POST'])
@views.route('/home/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        desc = request.form['post']
        db.session.add(Post(desc=desc, userName=current_user.userName, userpic=current_user.profilePic))
        db.session.commit()
    posts = get_posts_for_user(current_user)
    likedPosts = get_posts_liked_by_users(current_user)
    disLikedPosts = get_posts_disliked_by_users(current_user)
    suggestions = get_users_suggestions(current_user)
    return render_template('home.html', user=current_user, posts=posts, likedPosts=likedPosts, disLikedPosts=disLikedPosts, sugs=suggestions)

@views.route('/<username>/')
@login_required
def profile(username):
    suggestions = get_users_suggestions(current_user)
    user = User.query.filter_by(userName=username).first()
    likedPosts = get_posts_liked_by_users(current_user)
    disLikedPosts = get_posts_disliked_by_users(current_user)
    return render_template('profile.html', user=user, sugs=suggestions, likedPosts=likedPosts, disLikedPosts=disLikedPosts)

@views.route('/post/<postId>/')
@login_required
def post(postId):
    post = Post.query.filter_by(id=postId).first()
    likedPosts = get_posts_liked_by_users(current_user)
    disLikedPosts = get_posts_disliked_by_users(current_user)
    suggestions = get_users_suggestions(current_user)
    return render_template('post.html', user=current_user, likedPosts=likedPosts, disLikedPosts=disLikedPosts, post=post, sugs=suggestions)


@views.route('/following/')
@login_required
def following():
    usersFollowing = get_users_following(current_user)
    suggestions = get_users_suggestions(current_user)
    return render_template('following.html', user=current_user, usersFollowing=usersFollowing, sugs=suggestions)

@views.route('/message/', methods=['POST', 'GET'])
@login_required
def message():
    messageReqs = get_message_requests(current_user)
    return render_template('message.html', user=current_user, usersFollowing=get_users_following(current_user), msgReqs=messageReqs, sugs=get_users_suggestions(current_user))

@views.route('/messages/<toUserName>', methods=['POST', 'GET'])
@login_required
def messages(toUserName):
    toUser = User.query.filter_by(userName=toUserName).first()
    if request.method == 'POST':
        msg = request.form['msg']
        db.session.add(Message(fromUserId=current_user.id, toUserId=toUser.id, msg=msg))
        db.session.commit()
    msgs = get_messages_for_user(current_user, toUser)
    return render_template('messages.html', user=current_user, toUser=toUser, msgs=msgs)

@views.route('/image/<file>/')
@login_required
def get_image(file):
    return send_from_directory("F:\\PyFlaskProjects\\MateSet\\website\\static\\images", file)