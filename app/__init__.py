import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML

# from app.models import db, mongo
# from app.schemas import ma
from app.extensions import db, mongo, ma
from app.graphql.queries import listProducts_resolver

load_dotenv()

query = ObjectType("Query")
query.set_field("listProducts", listProducts_resolver)

type_defs = load_schema_from_path("schemas.graphql")
schema = make_executable_schema(
    type_defs, query, snake_case_fallback_resolvers
)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, supports_credentials=True)
    app.secret_key = os.getenv("SESSION_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    mongo.init_app(app)
    app.config["SESSION_SQLALCHEMY"] = db

    # sess.init_app(app)
    api = Api(app)

    # from .resources.config import PlanConfig, PlanConfigList
    # from .resources.selections import PlanSelections, CoverageBenefitSelections, ProvisionSelections

    # from .resources.workflow.rating.GroupResource import Group
    # from .resources.workflow.rating.ProvisionResource import Provision, ProvisionList
    # from .resources.workflow.rating.PlanResource import Plan
    # from .resources.workflow.rating.PlanRateResource import PlanRate
    # from .resources.workflow.rating.BenefitResource import BenefitsList
    # from .resources.workflow.rating.FactorResource import FactorCalculator
    # from .resources.admin.CreateTables import CreateTables
    # from .resources.admin.ProductConfig import ProductConfig, ProductConfigList

    from .products.admin import CreateTables
    from .products.config import PlanConfig, PlanConfigList
    from .products.selections import PlanSelections, CoverageBenefitSelections, ProvisionSelections, RatingCalculatorResource, AgeBandsSelections, RateTableList

    api.add_resource(CreateTables, '/admin/create-tables')

    api.add_resource(PlanConfigList, '/config/plans')
    api.add_resource(PlanConfig, '/config/plan/<id>')
    api.add_resource(RateTableList, '/config/rate-table')

    api.add_resource(PlanSelections, '/selections/plan')
    api.add_resource(AgeBandsSelections, '/selections/age-bands')
    api.add_resource(CoverageBenefitSelections, '/selections/benefits')
    api.add_resource(ProvisionSelections, '/selections/provisions')
    api.add_resource(RatingCalculatorResource, '/rating-calculator')

    # api.add_resource(Group, '/workflow/group')
    # api.add_resource(Plan, '/workflow/plan')
    # api.add_resource(PlanRate, '/workflow/plan-rate')
    # api.add_resource(ProvisionList, '/workflow/provisions')
    # api.add_resource(BenefitsList, '/workflow/benefits')
    # api.add_resource(FactorCalculator, '/workflow/factor-calc')
    # api.add_resource(CreateTables, '/admin/create-tables')
    # api.add_resource(ProductConfig, '/admin/product')
    # api.add_resource(ProductConfigList, '/admin/products')

    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return PLAYGROUND_HTML, 200

    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()
        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=app.debug
        )
        status_code = 200 if success else 400
        return jsonify(result), status_code
    return app
