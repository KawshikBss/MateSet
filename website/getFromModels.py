from .models import User, Post, Message, Activity
from .dateFunction import is_recent
from . import db
import random

def get_users_following(user):
    nameUsersFollowing = get_users_following_name(user)
    users = User.query.all()
    return [usr for usr in users if usr.userName in nameUsersFollowing][::-1]

def get_users_following_name(user):
    following = user.following
    return [usr.followedUser for usr in following][::-1]

def get_users_suggestions(user):
    usersFollowing = get_users_following_name(user)
    users = User.query.all()
    suggestions = [sug for sug in users if not sug.id == user.id and sug.userName not in usersFollowing]
    suggestions = suggestions[:10]
    random.shuffle(suggestions)
    return suggestions

def get_posts_for_user(user):
    usersFollowing = get_users_following_name(user)
    posts = Post.query.all()
    if posts:
        posts = [post for post in posts if (post.userName in usersFollowing or post.userName == user.userName) and is_recent(post.postDate)]
        return posts[::-1]
    else:
        return []

def get_post_reacts(post, user):
    reacts = [False, False]
    for like in post.liked:
        if like.user == user.userName:
            reacts[0] = like
            break

    for disLike in post.disLiked:
        if disLike.user == user.userName:
            reacts[1] = disLike
            break
    return reacts

def get_posts_liked_by_users(user):
    return [like.post for like in user.liked]

def get_posts_disliked_by_users(user):
    return [disLike.post for disLike in user.disLiked]

def get_messages_for_user(user, otherUser):
    allMsgs = Message.query.all()
    msgs = [msg for msg in allMsgs if (msg.fromUserId == user.id and msg.toUserId == otherUser.id) or (msg.fromUserId == otherUser.id and msg.toUserId == user.id)]
    return msgs

def get_message_requests(user):
    allMsgs = Message.query.filter_by(toUserId=user.id).all()
    usersFollowing = get_users_following(user)
    users = []
    for msg in allMsgs:
        tmpUser = User.query.filter_by(id=msg.fromUserId).first()
        if tmpUser not in users and tmpUser not in usersFollowing:
            users.append(tmpUser)
    return users[::-1]

def get_activities(user):
    activitis = user.activities
    return [act for act in activitis if is_recent(act.activityDate)][::-1]