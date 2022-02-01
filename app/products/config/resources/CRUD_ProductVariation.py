from flask import request
from flask_restful import Resource
from app.shared import CRUD_ResourceFactory

from ..models import Model_ConfigProductVariation, Model_ConfigAttributeDistributionSet
from ..schemas import Schema_ConfigProductVariation

_config_schema = Schema_ConfigProductVariation()
_Standard_CRUD_Config_ProductVariation = CRUD_ResourceFactory(
    resource_name='_Standard_CRUD_Config_ProductVariation', 
    model=Model_ConfigProductVariation, 
    schema=Schema_ConfigProductVariation,
    primary_key='product_variation_id'
).generate_class()

class CRUD_ProductVariation(_Standard_CRUD_Config_ProductVariation):

    @classmethod
    def post(cls):
        req = request.get_json()
        if not req.get('sex_distinct_distribution_set_id'): 
            sex_distinct = Model_ConfigAttributeDistributionSet.find_by_attr_type('gender', True)
            req['sex_distinct_distribution_set_id'] = sex_distinct[0].attr_distribution_set_id
        if not req.get('smoker_distinct_distribution_set_id'): 
            smoker_distinct = Model_ConfigAttributeDistributionSet.find_by_attr_type('smoker_status', True)
            req['smoker_distinct_distribution_set_id'] = smoker_distinct[0].attr_distribution_set_id

        variation = _config_schema.load(req)
        variation.save_to_db()
        return _config_schema.dump(variation), 200
