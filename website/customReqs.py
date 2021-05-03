from flask import Blueprint, request, jsonify, json
from flask_login import current_user
from .models import User, Follow, Post, Like, DisLike, Activity
from . import db
from .getFromModels import *

# defined as blueprint
customReqs = Blueprint('customReqs', __name__)

# creating route to recieve custom request from json
@customReqs.route('/like-post', methods=['POST'])
def like_post():
    post = json.loads(request.data)['postId']
    tmpPost = Post.query.filter_by(id=post).first()
    ifUser = get_post_reacts(tmpPost, current_user)
    
    if not ifUser[0] and not ifUser[1]:
        tmpPost.likes += 1
        db.session.add(Like(post=post, user=current_user.userName))
        db.session.add(Activity(fromUser=current_user.userName, toUser=tmpPost.userName, desc=f'{ current_user.userName } liked your post', link=f'/post/{ post }/'))
    elif ifUser[0] and not ifUser[1]:
        tmpPost.likes -= 1
        db.session.delete(ifUser[0])
    elif not ifUser[0] and ifUser[1]:
        tmpPost.likes += 1
        tmpPost.disLikes -= 1
        db.session.add(Like(post=post, user=current_user.userName))
        db.session.add(Activity(fromUser=current_user.userName, toUser=tmpPost.userName, desc=f'{ current_user.userName } liked your post', link=f'/post/{ post }/'))
        db.session.delete(ifUser[1])

    db.session.commit()

    return jsonify({})

@customReqs.route('/dis-like-post', methods=['POST'])
def dis_like_post():
    post = json.loads(request.data)['postId']
    tmpPost = Post.query.filter_by(id=post).first()
    ifUser = get_post_reacts(tmpPost, current_user)
    if not ifUser[0] and not ifUser[1]:
        tmpPost.disLikes += 1
        db.session.add(DisLike(post=post, user=current_user.userName))
        db.session.add(Activity(fromUser=current_user.userName, toUser=tmpPost.userName, desc=f'{ current_user.userName } disliked your post', link=f'/post/{ post }/'))
    
    elif ifUser[0] and not ifUser[1]:
        tmpPost.disLikes += 1
        tmpPost.likes -= 1
        db.session.add(DisLike(post=post, user=current_user.userName))
        db.session.add(Activity(fromUser=current_user.userName, toUser=tmpPost.userName, desc=f'{ current_user.userName } disliked your post', link=f'/post/{ post }/'))
        db.session.delete(ifUser[0])

    elif not ifUser[0] and ifUser[1]:
        tmpPost.disLikes -= 1
        db.session.delete(ifUser[1])

    db.session.commit()

    return jsonify({})

@customReqs.route('/follow-user', methods=['POST'])
def follow_user():
    targetId = json.loads(request.data)['targetId']
    followedUser = User.query.filter_by(id=targetId).first().userName
    db.session.add(Follow(user=current_user.userName, followedUser=followedUser))
    db.session.add(Activity(fromUser=current_user.userName, toUser=followedUser, desc=f'{ current_user.userName } followed you', link=f'/{ current_user.userName }/'))
    db.session.commit()

    return jsonify({})

@customReqs.route('/unfollow-user', methods=['POST'])
def unfollow_user():
    targetId = json.loads(request.data)['targetId']
    followedUser = User.query.filter_by(id=targetId).first()
    toDelete = Follow.query.filter_by(user=current_user.userName, followedUser=followedUser.userName).first()
    db.session.delete(toDelete)
    db.session.commit()

    return jsonify({})