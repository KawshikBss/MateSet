from flask import Blueprint, render_template

# defining blueprint
auth = Blueprint("auth", __name__)

# defining route to login
@auth.route("/login/")
def login():
    return render_template("login.html")