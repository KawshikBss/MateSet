from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from os import path

# creating database object
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    """To crate a Flask app

    Returns:
        app: a flask app
    """    
    # creating Flask app
    app = Flask(__name__)

    # confiuring app secret key
    app.config['SECRET_KEY'] = "Lucifer Morningstar"

    # configuring sqlite database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    # creating db files
    create_db(app)

    # returning app
    return app

def create_db(app):
    """To create db schemas

    Args:
        app (Flask): flask app
    """    
    if not path.exists('websites/' + DB_NAME):
        db.create_all(app=app)