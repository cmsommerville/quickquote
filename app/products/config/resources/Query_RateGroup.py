from flask import request
from flask_restful import Resource

from ..models import Model_ConfigRateGroup
from ..schemas import Schema_ConfigRateGroup

config_schema = Schema_ConfigRateGroup()
config_schema_list = Schema_ConfigRateGroup(many=True)


class Query_AllRateGroups(Resource):

    @classmethod
    def get(cls):
        product_id = request.args.get('product_id')
        res = Model_ConfigRateGroup.find_by_product(product_id)
        return config_schema_list.dump(res), 200

