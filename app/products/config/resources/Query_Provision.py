from flask import request
from flask_restful import Resource

from ..models import Model_ConfigProvision
from ..schemas import Schema_ConfigProvision

config_schema = Schema_ConfigProvision()
config_schema_list = Schema_ConfigProvision(many=True)

class Query_ProvisionStateConfig(Resource):

    @classmethod
    def get(cls):
        product_id = request.args.get('product_id')
        state = request.args.get('state')
        effective_date = request.args.get('effective_date')
        res = Model_ConfigProvision.find_by_state(state, effective_date, product_id)
        return config_schema_list.dump(res), 200
