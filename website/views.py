from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
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

@views.route('/settings/', methods=['POST', 'GET'])
@login_required
def settings():
    if request.method == 'POST':
        currPassword = request.form['curpassword']
        if not currPassword:
            flash("Must confirm current password to save changes")
        else:
            if check_password_hash(current_user.password, currPassword):
                newUserName = request.form['username']
                if newUserName:
                    if len(newUserName) < 2:
                        flash("Username is too short")
                    else:
                        if newUserName == current_user.userName:
                            flash("You are already using this user name")
                        else:
                            alreadyExists = User.query.filter_by(userName=newUserName).first()
                            if alreadyExists:
                                flash("User name already exists")
                            else:
                                current_user.userName = newUserName
                                flash(f"User name changed to {newUserName}")
                newName = request.form['name']
                if newName:
                    if ' ' not in newName:
                        flash("First name and Last name  ust be included in name")
                    else:
                        current_user.name = newName
                        flash(f"Name changed to {newName}")
                newEmail = request.form['email']
                if newEmail:
                    if '@' in newEmail and '.com' in newEmail:
                        emailAlreadyExists = User.query.filter_by(email=newEmail).first()
                        if emailAlreadyExists:
                            flash("Email already exists")
                        else:
                            current_user.email = newEmail
                            flash("Email changed")
                newPassword = request.form['password']
                if newPassword:
                    if len(newPassword) < 8:
                        flash("Password must be atleast 8 characters")
                    else:
                        if check_password_hash(current_user.password, newPassword):
                            flash("This is the current password")
                        else:
                            current_user.password = generate_password_hash(newPassword, method='sha256')
                            flash("Password changed")
                db.session.commit()
            else:
                flash("Current password doesn't match")
        
    return render_template('settings.html', user=current_user)

@views.route('/following/')
@login_required
def following():
    usersFollowing = get_users_following(current_user)
    suggestions = get_users_suggestions(current_user)
    return render_template('following.html', user=current_user, usersFollowing=usersFollowing, sugs=suggestions)