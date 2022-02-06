from flask import request
from flask_restful import Resource
from app.shared import CRUD_ResourceFactory

from ..models import Model_ConfigBenefit
from ..schemas import Schema_ConfigBenefit

_config_schema_list = Schema_ConfigBenefit(many=True)
_Standard_CRUD_Config_Benefit_List = CRUD_ResourceFactory(
    resource_name='_Standard_CRUD_Config_Benefit_List', 
    model=Model_ConfigBenefit, 
    schema=Schema_ConfigBenefit,
    primary_key='benefit_id'
).generate_list_class()

class CRUD_ProductVariation(_Standard_CRUD_Config_Benefit_List):

    @classmethod
    def post(cls):
        req = request.get_json()
        try: 
            codes = set([item['benefit_code'] for item in req])
            benefit_code = codes[0]
            assert(len(set([item['benefit_code'] for item in req])) == 1)
        except: 
            raise Exception("Only one benefit code can be processed at one time")
        benefits = _config_schema_list.load(req)
        Model_ConfigBenefit.delete_by_benefit_code(benefit_code)
        Model_ConfigBenefit.save_all_to_db()
        return _config_schema_list.dump(benefits), 200
