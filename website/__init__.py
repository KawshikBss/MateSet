from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

# creating database object
bd = SQLAlchemy()
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

    # returning app
    return app