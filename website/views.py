from flask import Blueprint, render_template

# defining blueprint
views = Blueprint("views", __name__)

# defining route to homepage
@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")