from flask import request
from flask_restful import Resource

from ..models import Model_ConfigAgeBandSet
from ..schemas import Schema_ConfigAgeBandSet
from ...queries.Config_AllAgeBands import query_config_age_bands

_config_schema = Schema_ConfigAgeBandSet()
_config_schema_list = Schema_ConfigAgeBandSet(many=True)

class Query_AgeBandsStateConfig(Resource):

    @classmethod
    def get(cls):
        product_variation_id = request.args.get('product_variation_id')
        state = request.args.get('state')
        effective_date = request.args.get('effective_date')
        res = Model_ConfigAgeBandSet.find_by_state(state, effective_date, product_variation_id)
        return _config_schema_list.dump(res), 200

class Query_AllAgeBands(Resource):

    @classmethod
    def get(cls):
        product_variation_id = request.args.get('product_variation_id')
        res = Model_ConfigAgeBandSet.find_by_variation(product_variation_id)
        return _config_schema_list.dump(res), 200


class Query_AllAgeBandsByProduct(Resource):

    @classmethod
    def get(cls, product_id: int):
        res = query_config_age_bands(product_id).all()
        return _config_schema_list.dump(res), 200
