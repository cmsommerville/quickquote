from flask import request
from flask_restful import Resource

from ..models import Model_ConfigBenefit
from ..schemas import Schema_ConfigBenefit

config_benefit_schema_list = Schema_ConfigBenefit(many=True)

class CRUD_BenefitStateAvailabilityConfig(Resource):

    @classmethod
    def get(cls, id):
        config = Model_ConfigBenefit.find_child_states(id)
        return config_benefit_schema_list.dump(config), 200

