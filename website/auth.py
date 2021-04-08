from flask import Blueprint, render_template, request, flash
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

# defining blueprint
auth = Blueprint("auth", __name__)

# defining route to login
@auth.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(userName = username).first()
        if user:
            flash("Logged in successfully")
    return render_template("login.html")

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

    return render_template("signup.html")