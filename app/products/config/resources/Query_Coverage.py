from flask import request
from flask_restful import Resource

from ..models import Model_ConfigCoverage
from ..schemas import Schema_ConfigCoverage

config_schema = Schema_ConfigCoverage()
config_schema_list = Schema_ConfigCoverage(many=True)



class Query_AllCoverages(Resource):

    @classmethod
    def get(cls):
        product_variation_id = request.args.get('product_variation_id')
        res = Model_ConfigCoverage.find_by_variation(product_variation_id)
        return config_schema_list.dump(res), 200

class Query_CoverageStateConfig(Resource):

    @classmethod
    def get(cls):
        product_id = request.args.get('product_id')
        state = request.args.get('state')
        effective_date = request.args.get('effective_date')
        res = Model_ConfigCoverage.find_by_state(state, effective_date, product_id)
        return config_schema_list.dump(res), 200
