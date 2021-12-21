from flask import request
from flask_restful import Resource

from ..models import Model_ConfigFactor
from ..schemas import Schema_ConfigFactor

config_schema = Schema_ConfigFactor()
config_schema_list = Schema_ConfigFactor(many=True)



class Query_AllFactors(Resource):

    @classmethod
    def get(cls):
        provision_id = request.args.get('provision_id')
        res = Model_ConfigFactor.find_by_provision(provision_id)
        return config_schema_list.dump(res), 200

