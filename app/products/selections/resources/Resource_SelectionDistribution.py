from flask import request, session
from flask_restful import Resource

from ..models import Model_SelectionDistribution, Model_SelectionPlan
from ..schemas import Schema_SelectionDistribution


_selection_schema_list = Schema_SelectionDistribution(many=True)


def _smoker_status_handler(plan_id: int, pct_ns: float): 
    return [
        {
            "selection_plan_id": plan_id,
            "attr_type_code": "smoker_status", 
            "attr_value": "N", 
            "weight": pct_ns
        },
        {
            "selection_plan_id": plan_id,
            "attr_type_code": "smoker_status", 
            "attr_value": "T", 
            "weight": 100-pct_ns
        }
    ]


def _gender_handler(plan_id: int, pct_m: float): 
    return [
        {
            "selection_plan_id": plan_id,
            "attr_type_code": "gender", 
            "attr_value": "M", 
            "weight": pct_m
        },
        {
            "selection_plan_id": plan_id,
            "attr_type_code": "gender", 
            "attr_value": "F", 
            "weight": 100-pct_m
        }
    ]

class Resource_SelectionDistribution(Resource):

    @classmethod
    def get(cls, plan_id):
        dist = Model_SelectionDistribution.find_by_plan(plan_id)

        return _selection_schema_list.dump(dist), 200

    @classmethod
    def post(cls, plan_id):
        if request.args.get('pct_ns', type=float): 
            data = _smoker_status_handler(plan_id, request.args.get('pct_ns', type=float))
            Model_SelectionDistribution.delete_by_plan(plan_id, 'smoker_status')
        elif request.args.get('pct_m', type=float): 
            data = _gender_handler(plan_id, request.args.get('pct_m', type=float))
            Model_SelectionDistribution.delete_by_plan(plan_id, 'gender')
        else: 
            data = request.get_json()
            Model_SelectionDistribution.delete_by_plan_attr(plan_id)

        dist = _selection_schema_list.load(data)
        Model_SelectionDistribution.save_all_to_db(dist)
        return _selection_schema_list.dump(dist), 201