import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_session import Session
from dotenv import load_dotenv

from app.models import db, mongo
from app.schemas import ma

load_dotenv()
sess = Session()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, origins=["http://localhost:8080"], supports_credentials=True)
    app.secret_key = os.getenv("SESSION_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    mongo.init_app(app)
    app.config["SESSION_SQLALCHEMY"] = db

    sess.init_app(app)
    api = Api(app)

    from .resources.workflow.rating.Group import Group
    from .resources.workflow.rating.Plan import Plan
    from .resources.workflow.rating.ProductFactors import ProductFactors
    from .resources.admin.CreateTables import CreateTables

    api.add_resource(Group, '/workflow/group')
    api.add_resource(Plan, '/workflow/plan')
    api.add_resource(ProductFactors, '/workflow/product-factors')
    api.add_resource(CreateTables, '/admin/create-tables')

    @app.route("/")
    def hello_world():
        return "<h1>Hello World!</h1>"

    return app
