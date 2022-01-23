import os
from sqlalchemy import event
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv

from app.extensions import db, ma, sess

load_dotenv()

def bindRoutes(api, routes, prefix=None):
    for route in routes: 
        api.add_resource(route['class'], *[
            prefix + route if prefix else route for route in route['endpoints']
        ])
        

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, supports_credentials=True)
    app.secret_key = os.getenv("SESSION_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    app.config["SESSION_SQLALCHEMY"] = db

    # sess.init_app(app)
    api = Api(app)

    from .products.admin import CreateTables, SessionData
    # from .products.selections import RateTableList
    # from .products.config.resources import routes as config_routes
    from .products.config.routes import routes as config_routes
    from .products.selections.resources import routes as selection_routes

    from .products.config.data.initialize import Resource_InitializeData
    
    # bindRoutes(api, config_routes)
    bindRoutes(api, config_routes)
    bindRoutes(api, selection_routes)

    api.add_resource(CreateTables, '/admin/create-tables')
    api.add_resource(SessionData, '/admin/session-data')
    # api.add_resource(RateTableList, '/config/rate-table')
    api.add_resource(Resource_InitializeData, '/config/initialize-data')

    return app
