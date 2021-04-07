from flask import Blueprint, render_template, redirect, url_for

# defining blueprint
views = Blueprint("views", __name__)

# defining route to homepage
@views.route("/")
@views.route("/home")
def home():
    return redirect(url_for("login.html"))