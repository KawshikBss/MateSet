from flask import Blueprint

# defining blueprint
views = Blueprint("views", __name__)

# defining route to homepage
@views.route("/")
@views.route("/home")
def home():
    return "<h1>Home</h1>"