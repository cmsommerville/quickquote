import os
from sqlalchemy import event
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML

from app.extensions import db, mongo, ma, sess, expire_old_records
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

    sess.init_app(app)
    api = Api(app)

    db.event.listen(db.session, "before_flush", expire_old_records)

    from .products.admin import CreateTables, SessionData
    from .products.config import PlanConfig, PlanConfigList
    from .products.selections import PlanSelections, CoverageBenefitSelections, ProvisionSelections, RatingCalculatorResource, AgeBandsSelections, RateTableList

    api.add_resource(CreateTables, '/admin/create-tables')
    api.add_resource(SessionData, '/admin/session-data')

    api.add_resource(PlanConfigList, '/config/plans')
    api.add_resource(PlanConfig, '/config/plan/<id>')
    api.add_resource(RateTableList, '/config/rate-table')

    api.add_resource(PlanSelections, '/selections/plan')
    api.add_resource(AgeBandsSelections, '/selections/age-bands')
    api.add_resource(CoverageBenefitSelections, '/selections/benefits')
    api.add_resource(ProvisionSelections, '/selections/provisions')
    api.add_resource(RatingCalculatorResource, '/rating-calculator')

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

    @app.route("/session/<id>", methods=["GET"])
    def getSessionData(id):
        data = session["PLAN-" + id]
        print(session)
        return jsonify(data), 200

    return app
