from flask import Flask
from flask_restful import Api


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/qq-dev.db'

    @app.route("/")
    def hello_world():
        return "<h1>Hello World!</h1>"

    return app
