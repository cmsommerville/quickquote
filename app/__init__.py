import os
from flask import Flask
from flask_restful import Api
from app.models import db, ma


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        "SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    @app.route("/")
    def hello_world():
        return "<h1>Hello World!</h1>"

    db.init_app(app)
    ma.init_app(app)

    from .resources.products.product_admin import ProductAdmin, ProductAdminList
    from .resources.benefits.benefit_admin import BenefitAdmin, BenefitAdminList
    from .resources.provisions.provision_admin import ProvisionAdmin, ProvisionAdminList
    from .resources.states.state_admin import StateAdmin, StateAdminList
    from .resources.claim_costs.claim_cost_admin import ClaimCostAdmin, ClaimCostAdminList

    api = Api(app)
    api.add_resource(ProductAdmin, '/api/v1/product')
    api.add_resource(ProductAdminList, '/api/v1/products')
    api.add_resource(BenefitAdmin, '/api/v1/benefit')
    api.add_resource(BenefitAdminList, '/api/v1/benefits')
    api.add_resource(ClaimCostAdmin, '/api/v1/claim_cost')
    api.add_resource(ClaimCostAdminList, '/api/v1/claim_costs')
    api.add_resource(ProvisionAdmin, '/api/v1/provision')
    api.add_resource(ProvisionAdminList, '/api/v1/provisions')
    api.add_resource(StateAdmin, '/api/v1/state')
    api.add_resource(StateAdminList, '/api/v1/states')

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app
