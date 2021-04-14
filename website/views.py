from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import User, Post
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
        db.session.add(Post(desc=desc, userName=current_user.userName))
        db.session.commit()
    posts = get_posts_for_user(current_user)
    suggestions = get_users_suggestions(current_user)
    return render_template('home.html', user=current_user, posts=posts, sugs=suggestions)

@views.route('/<username>/')
@login_required
def profile(username):
    suggestions = get_users_suggestions(current_user)
    user = User.query.filter_by(userName=username).first()
    return render_template('profile.html', user=user, sugs=suggestions)

@views.route('/following/')
@login_required
def following():
    usersFollowing = get_users_following(current_user)
    suggestions = get_users_suggestions(current_user)
    return render_template('following.html', user=current_user, usersFollowing=usersFollowing, sugs=suggestions)