from collections import defaultdict
from app.products.config.models.Config_ProductVariation import Model_ConfigProductVariation
from flask import request, session
from flask_restful import Resource

from ..errors import ERR1003, ERR1004
from ..models import Model_SelectionAgeBands, Model_SelectionPlan
from ..schemas import Schema_SelectionAgeBands, Schema_QueryAgeBands
from ...queries.Selection_AgeBands import query_config_benefits


_selection_schema_list = Schema_SelectionAgeBands(many=True)
_config_schema_list = Schema_QueryAgeBands(many=True)


class Resource_SelectionAgeBands(Resource):

    @classmethod
    def get(cls, plan_id):
        plan = Model_SelectionPlan.find_one(plan_id)
        if not plan: 
            return {
                "error_code": "ERR1004",
                "message": ERR1004.format(plan_id = plan_id)
            }, 400

        # if age bands have been previously selected, return them
        if len(plan.age_bands) > 0:
            return {"age_bands": _selection_schema_list.dump(plan.age_bands)}, 200

        # get the product variation and determine if age rated
        product_variation = Model_ConfigProductVariation.find_one(plan.config_product_variation_id)
        if not product_variation.is_age_rated: 
            return {
                "error_code": "ERR1003",
                "message": ERR1003.format(product_variation_code=product_variation.product_variation_code)
            }, 400
        
        # if age rated, then get the applicable configured age bands
        qry = query_config_benefits(plan)
        for row in qry.populate_existing(): 
            print(row)

        return next((x for x in _config_schema_list.dump(qry.populate_existing())), {}), 200

    @classmethod
    def post(cls, plan_id):
        data = request.get_json()
        age_bands = _selection_schema_list.load(data)
        Model_SelectionAgeBands.save_all_to_db(age_bands)
        return _selection_schema_list.dump(age_bands), 201