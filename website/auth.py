from flask import Blueprint, render_template, request
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
        print("Username = ", username, " Password = ", password)
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
            print("Name short")
        elif len(lname) <= 2:
            print("Name short")
        elif len(username) <= 2:
            print("Username short")
        elif '@' not in email and '.com' not in email:
            print("No such email")
        elif len(password) < 8:
            print("Password short")
        elif not password == confirm:
            print("No match")
        else:
            name = fname + " " + lname
            newUser = User(name=name, userName=username, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(newUser)
            db.session.commit()
            print("Everything ok")

    return render_template("signup.html")