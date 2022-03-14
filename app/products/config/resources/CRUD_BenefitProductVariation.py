from flask import request
from flask_restful import Resource

from ..models import Model_ConfigBenefitProductVariation
from ..schemas import Schema_ConfigBenefitProductVariation

_config_benefit_variation_schema_list = Schema_ConfigBenefitProductVariation(many=True)

class CRUD_BenefitProductVariationConfig(Resource):

    @classmethod
    def get(cls):
        product_variation_id = request.args.get('product_variation_id')
        if product_variation_id: 
            config = Model_ConfigBenefitProductVariation.find_benefits(product_variation_id)
            return _config_benefit_variation_schema_list.dump(config), 200

        
        benefit_id = request.args.get('benefit_id')
        if benefit_id: 
            config = Model_ConfigBenefitProductVariation.find_product_variations(benefit_id)
            return _config_benefit_variation_schema_list.dump(config), 200


    @classmethod
    def post(cls):
        data = request.get_json()
        benefit_variations = _config_benefit_variation_schema_list.load(data)
        Model_ConfigBenefitProductVariation.merge(benefit_variations)
        return _config_benefit_variation_schema_list.dump(benefit_variations), 200


    @classmethod
    def delete(cls):
        data = request.get_json()
        product_variation_id = request.args.get('product_variation_id')
        if product_variation_id:
            benefits = Model_ConfigBenefitProductVariation.find_benefits(product_variation_id)
            Model_ConfigBenefitProductVariation.delete_many(benefits)
        return "Deleted", 201
