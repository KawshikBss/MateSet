from flask import Flask

def create_app():
    # creating Flask app
    app = Flask(__name__)
    # confiuring app secret key
    app.config['SECRET_KEY'] = "Lucifer Morningstar"

    # returning app
    return app