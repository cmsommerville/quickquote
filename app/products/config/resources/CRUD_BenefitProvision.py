from flask import request
from flask_restful import Resource

from ..models import Model_ConfigBenefitProvision
from ..schemas import Schema_ConfigBenefitProvision

_config_schema_list = Schema_ConfigBenefitProvision(many=True)

class CRUD_BenefitProvisionConfig(Resource):

    @classmethod
    def get(cls):
        provision_id = request.args.get('provision_id')
        if provision_id: 
            config = Model_ConfigBenefitProvision.find_benefits(provision_id)
            return _config_schema_list.dump(config), 200

        
        benefit_id = request.args.get('benefit_id')
        if benefit_id: 
            config = Model_ConfigBenefitProvision.find_provisions(benefit_id)
            return _config_schema_list.dump(config), 200


    @classmethod
    def post(cls):
        data = request.get_json()
        benefit_provisions = _config_schema_list.load(data)
        Model_ConfigBenefitProvision.merge(benefit_provisions)
        return _config_schema_list.dump(benefit_provisions), 200
