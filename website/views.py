from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from .models import *
from . import db
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
    posts = Post.query.all()
    return render_template('home.html', user=current_user, posts=posts)

@views.route('/<username>/')
@login_required
def profile(username):
    return render_template('profile.html', user=current_user)