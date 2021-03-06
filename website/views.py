from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory
from flask_login import login_required, current_user
from .models import User, Post, Message, Comment, Activity, Follow
from . import db, UPLOADE_FOLDER
from .getFromModels import *
from .helper_functions import get_image_path
from werkzeug.utils import secure_filename
from os import path

# defining blueprint
views = Blueprint("views", __name__)

# defining route to homepage
@views.route('/', methods=['GET', 'POST'])
@views.route('/home/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        desc = request.form['post']
        postImg = request.files['image']
        if postImg.filename:
            fileName = get_image_path(postImg.filename)
            db.session.add(Post(desc=desc, userName=current_user.userName, userpic=current_user.profilePic, img=fileName))
            postImg.save(path.join(UPLOADE_FOLDER, secure_filename(fileName)))
        else:
            db.session.add(Post(desc=desc, userName=current_user.userName, userpic=current_user.profilePic))
        db.session.commit()
    posts = get_posts_for_user(current_user)
    likedPosts = get_posts_liked_by_users(current_user)
    disLikedPosts = get_posts_disliked_by_users(current_user)
    suggestions = get_users_suggestions(current_user)
    return render_template('home.html', user=current_user, posts=posts, likedPosts=likedPosts, disLikedPosts=disLikedPosts, sugs=suggestions, alerts=get_alerts(current_user))

@views.route('/search/', methods=['GET', 'POST'])
@login_required
def search():
    search = ''
    if request.method == 'POST':
        search = request.form['search']
    users = get_searched_users(search)
    usersFollowing = get_users_following(current_user)
    suggestions = get_users_suggestions(current_user)
    return render_template('search.html', user=current_user, users=users, usersFollowing=usersFollowing, sugs=suggestions, alerts=get_alerts(current_user))

@views.route('/<username>/')
@login_required
def profile(username):
    suggestions = get_users_suggestions(current_user)
    user = User.query.filter_by(userName=username).first()
    likedPosts = get_posts_liked_by_users(current_user)
    disLikedPosts = get_posts_disliked_by_users(current_user)
    return render_template('profile.html', user=current_user, profileUser=user, sugs=suggestions, likedPosts=likedPosts, disLikedPosts=disLikedPosts, alerts=get_alerts(current_user))

@views.route('/post/<postId>/', methods=['POST', 'GET'])
@login_required
def post(postId):
    post = Post.query.filter_by(id=postId).first()
    if request.method == 'POST':
        comment = request.form['comment']
        if len(comment) > 0:
            db.session.add(Comment(desc=comment, postId=postId, userName=current_user.userName))
            db.session.add(Activity(fromUser=current_user.userName, toUser=post.userName, desc=f'{ current_user.userName } commented on your post', link=f'/post/{ postId }/'))
            post.comments += 1
            db.session.commit()
        else:
            flash("Cannot post an empty comment")
    likedPosts = get_posts_liked_by_users(current_user)
    disLikedPosts = get_posts_disliked_by_users(current_user)
    suggestions = get_users_suggestions(current_user)
    return render_template('post.html', user=current_user, likedPosts=likedPosts, disLikedPosts=disLikedPosts, post=post, sugs=suggestions, alerts=get_alerts(current_user))

@views.route('/edit-post/<postId>/', methods=['POST', 'GET'])
@login_required
def edit_post(postId):
    post = Post.query.filter_by(id=postId).first()
    if request.method == 'POST':
        desc = request.form['desc']
        img = request.files['image']
        if desc or img:
            if len(desc) > 0 and desc:
                post.desc = desc
            if img.filename:
                fileName = get_image_path(img.filename)
                post.img = fileName
                img.save(path.join(UPLOADE_FOLDER, secure_filename(fileName)))
            db.session.commit()
        else:
            flash("No changes were made")
    likedPosts = get_posts_liked_by_users(current_user)
    disLikedPosts = get_posts_disliked_by_users(current_user)
    suggestions = get_users_suggestions(current_user)
    return render_template('edit-post.html', user=current_user, likedPosts=likedPosts, disLikedPosts=disLikedPosts, post=post, sugs=suggestions, alerts=get_alerts(current_user))

@views.route('/activities/')
@login_required
def activities():
    suggestions = get_users_suggestions(current_user)
    return render_template('activities.html', user=current_user, acts=get_activities(current_user), sugs=suggestions, alerts=get_alerts(current_user))

@views.route('/following/')
@login_required
def following():
    usersFollowing = get_users_following(current_user)
    suggestions = get_users_suggestions(current_user)
    return render_template('following.html', user=current_user, usersFollowing=usersFollowing, sugs=suggestions, alerts=get_alerts(current_user))

@views.route('/message/', methods=['POST', 'GET'])
@login_required
def message():
    searchedUsers = []
    if request.method == 'POST':
        searched = request.form['searchedUsers']
        users = get_searched_users(searched)
        usersFollowing = get_users_following_name(current_user)
        for usr in users:
            if usr.userName in usersFollowing:
                searchedUsers.append(usr)
    messageReqs = get_message_requests(current_user)
    return render_template('message.html', user=current_user, searchedUsers=searchedUsers, usersFollowing=get_users_following(current_user), usersMessagedBy = get_users_messaged_by(current_user), msgReqs=messageReqs, sugs=get_users_suggestions(current_user), alerts=get_alerts(current_user))

@views.route('/messages/<toUserName>', methods=['POST', 'GET'])
@login_required
def messages(toUserName):
    toUser = User.query.filter_by(userName=toUserName).first()
    if request.method == 'POST':
        msg = request.form['msg']
        img = request.files['image']
        if img.filename:
            fileName = get_image_path(img.filename)
            db.session.add(Message(fromUserId=current_user.id, toUserId=toUser.id, msg=msg, img=fileName))
            img.save(path.join(UPLOADE_FOLDER, secure_filename(fileName)))
        else:
            db.session.add(Message(fromUserId=current_user.id, toUserId=toUser.id, msg=msg))
        if toUserName not in get_users_following_name(current_user):
            db.session.add(Follow(user=current_user.userName, followedUser=toUserName))
        db.session.commit()
    msgs = get_messages_for_user(current_user, toUser)
    return render_template('messages.html', user=current_user, toUser=toUser, msgs=msgs)

@views.route('/image/<file>/')
@login_required
def get_image(file):
    return send_from_directory(UPLOADE_FOLDER, file)