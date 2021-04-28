from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from os import path

# defining blueprint
auth = Blueprint("auth", __name__)

# defining route to login
@auth.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(userName = username).first()
        if not user:
            flash("Incorrect username")
        else:
            if not check_password_hash(user.password, password):
                flash("Incorrect password")
            else:
                login_user(user=user, remember=True)
                flash("Logged in successfully")
                return redirect(url_for('views.home'))
    return render_template('login.html')

@auth.route('/logout/')
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for('auth.login'))

@auth.route('/signup/', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if len(fname) <= 2:
            flash("First name is too short")
        elif len(lname) <= 2:
            flash("Last name is too short")
        elif len(username) <= 2:
            flash("Username is too short")
        elif '@' not in email and '.com' not in email:
            flash("Incorrect email format")
        elif len(password) < 8:
            flash("Password is too short")
        elif not password == confirm:
            flash("Password does not match")
        else:
            name = fname + " " + lname
            userNameCheck = User.query.filter_by(userName=username).first()
            if not userNameCheck:
                emailCheck = User.query.filter_by(email=email).first()
                if not emailCheck:
                    newUser = User(name=name, userName=username, email=email, password=generate_password_hash(password, method='sha256'))
                    db.session.add(newUser)
                    db.session.commit()
                    flash("Sign Up successfull")
                else:
                    flash("Email already exists")
            else:
                flash("Username is taken")

    return render_template('signup.html')

@auth.route('/settings/', methods=['POST', 'GET'])
@login_required
def settings():
    if request.method == 'POST':
        currPassword = request.form['curpassword']
        if not currPassword:
            flash("Must confirm current password to save changes")
        else:
            if check_password_hash(current_user.password, currPassword):
                profilePic = request.files['profilePic']
                if profilePic.filename:
                    current_user.profilePic = profilePic.filename.replace(' ', '_')
                    for post in current_user.posts:
                        post.userpic = profilePic.filename
                    profilePic.save(path.join("F:\\PyFlaskProjects\\MateSet\\website\\static\\images", secure_filename(profilePic.filename.replace(' ', '_'))))
                    db.session.add(Post(desc=f'{ current_user.userName } changed his profile picture', userName=current_user.userName, userpic=profilePic.filename.replace(' ', '_'), img=profilePic.filename.replace(' ', '_')))
                    flash("Profile picture changed")
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

    userPosts = current_user.posts
        
    return render_template('settings.html', user=current_user)