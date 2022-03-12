from flask import request
from flask_restful import Resource

from ..models import Model_ConfigAgeDistributionSet, Model_ConfigAttributeDistributionSet
from ..schemas import Schema_ConfigAgeDistributionSet, Schema_ConfigAttributeDistributionSet

_config_attr_schema_list = Schema_ConfigAttributeDistributionSet(many=True)
_config_age_schema_list = Schema_ConfigAgeDistributionSet(many=True)

class Query_AgeDistributionSets(Resource):

    @classmethod
    def get(cls):
        res = Model_ConfigAgeDistributionSet.find_all()
        return _config_age_schema_list.dump(res), 200

class Query_AttrDistributionSets(Resource):

    @classmethod
    def get(cls):
        attr_code = request.args.get('attr_code')
        res = Model_ConfigAttributeDistributionSet.find_by_attr_type(attr_code)
        return _config_attr_schema_list.dump(res), 200