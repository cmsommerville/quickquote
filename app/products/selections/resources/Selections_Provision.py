import requests
from flask import request, session
from flask_restful import Resource

from ..models.Model_SelectionPlan import PlanModel
from ..schemas.Schema_SelectionPlan import PlanSchema
from ..models.Model_SelectionProvision import ProvisionModel
from ..schemas.Schema_SelectionProvision import ProvisionSchema

provision_list_schema = ProvisionSchema(many=True)
plan_schema = PlanSchema()


def mergeConfigAndSelections(config: list, selections: list) -> list:
    provisions = []
    selection_map = {prov['provision_code']: prov['provision_value'] for prov in selections}
    for item in config:
        prov = {**item}
        if selection_map.get(item['code']):
            prov['selectedValue'] = selection_map.get(item['code'])
        provisions.append(prov)


class ProvisionSelections(Resource):

    @classmethod
    def get(cls):
        plan_id = request.args.get("plan_id", type=int)
        plan_config_id = request.args.get("plan_config_id")
        # if a new plan request
        if plan_id is None:
            raise Exception("Please provide a plan ID query parameter")

        # if data exists in session
        session_data = session.get(plan_id)
        if session_data:
            return {"provisions": [], **session_data}

        # if looking up a plan not in session
        provisions = ProvisionModel.find_plan_provisions(plan_id)
        plan = PlanModel.find_by_id(plan_id)
        config = requests.get(
            f"{request.url_root}config/plan/{plan_config_id}").json()

        return {
            "plan": plan_schema.dump(plan),
            "plan_config": config,
            "provisions": mergeConfigAndSelections(config['provisions'], provision_list_schema.dump(provisions))
        }, 200

    @classmethod
    def post(cls):
        data = request.get_json()
        try:
            plan_id = data[0]["plan_id"]
        except Exception as e:
            return str(e), 400

        session_data = session.get(int(plan_id))

        try:
            provisions = provision_list_schema.load(data)
            ProvisionModel.save_all_to_db(provisions, plan_id)
            session[int(plan_id)] = {**session_data,
                                     "provisions": provision_list_schema.dump(provisions)}
        except Exception as e:
            return str(e), 400

        return "created", 201
