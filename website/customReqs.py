from flask import Blueprint, request, jsonify, json
from flask_login import current_user
from .models import User, Post, Like
from . import db

# defined as blueprint
customReqs = Blueprint('customReqs', __name__)

# creating route to recieve custom request from json
@customReqs.route('/like-post', methods=['POST'])
def like_post():
    post = json.loads(request.data)['postId']
    tmpPost = Post.query.filter_by(id=post).first()
    ifUser = [like for like in tmpPost.liked if like.user == current_user.userName]
    if ifUser:
        tmpPost.likes -= 1
        db.session.delete(ifUser[0])
    else:
        tmpPost.likes += 1
        db.session.add(Like(post=post, user=current_user.userName))
    db.session.commit()

    return jsonify({})