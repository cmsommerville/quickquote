import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv

from app.models import db, mongo
from app.schemas import ma
from app.extensions import sess

load_dotenv()


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

    from .resources.config import PlanConfig, PlanConfigList
    from .resources.selections import PlanSelections, CoverageBenefitSelections, ProvisionSelections

    from .resources.workflow.rating.GroupResource import Group
    from .resources.workflow.rating.ProvisionResource import Provision, ProvisionList
    from .resources.workflow.rating.PlanResource import Plan
    from .resources.workflow.rating.PlanRateResource import PlanRate
    from .resources.workflow.rating.BenefitResource import BenefitsList
    from .resources.workflow.rating.FactorResource import FactorCalculator
    from .resources.admin.CreateTables import CreateTables
    from .resources.admin.ProductConfig import ProductConfig, ProductConfigList

    api.add_resource(PlanConfigList, '/config/plans')
    api.add_resource(PlanConfig, '/config/plan/<id>')

    api.add_resource(PlanSelections, '/selections/plan')
    api.add_resource(CoverageBenefitSelections, '/selections/benefits')
    api.add_resource(ProvisionSelections, '/selections/provisions')

    api.add_resource(Group, '/workflow/group')
    api.add_resource(Plan, '/workflow/plan')
    api.add_resource(PlanRate, '/workflow/plan-rate')
    api.add_resource(ProvisionList, '/workflow/provisions')
    api.add_resource(BenefitsList, '/workflow/benefits')
    api.add_resource(FactorCalculator, '/workflow/factor-calc')
    api.add_resource(CreateTables, '/admin/create-tables')
    api.add_resource(ProductConfig, '/admin/product')
    api.add_resource(ProductConfigList, '/admin/products')

    @app.route("/")
    def hello_world():
        return "<h1>Hello World!</h1>"

    return app
