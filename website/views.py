from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

# defining blueprint
views = Blueprint("views", __name__)

# defining route to homepage
@views.route('/')
@views.route('/home/')
@login_required
def home():
    return render_template('home.html', user=current_user)