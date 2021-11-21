import requests
from flask import request, session
from flask_restful import Resource

from ..models.PlanModel import PlanModel
from ..schemas.PlanSchema import PlanSchema
from ...config import Config_PlanSchema

# from app.data.policy import policy

plan_schema = PlanSchema()


class PlanSelections(Resource):

    @classmethod
    def get(cls):
        plan_id = request.args.get("plan_id", type=int)
        plan_config_id = request.args.get("plan_config_id", type=str)

        # if a new plan request
        if plan_id is None:
            # get plan config
            if plan_config_id:
                config = requests.get(
                    f"{request.url_root}config/plan/{plan_config_id}").json()

                return {
                    "plan": {},
                    "plan_config": config
                }

            config = requests.get(
                f"{request.url_root}config/plans").json()

            return {
                "plan": {},
                "plan_config": config
            }

        # if data exists in session
        if session.get(plan_id):
            print("session")
            session_data = session.get(plan_id)
            if session_data:
                return session_data

        # if looking up a plan not in session
        try:
            print("fetch from db")
            plan = PlanModel.find_by_id(plan_id)
            plan_config_id = plan.plan_config_id
            config = requests.get(
                f"{request.url_root}config/plan/{plan_config_id}").json()

            return {
                "plan": plan_schema.dump(plan),
                "plan_config": config
            }, 200
        except:
            return None, 200

    def post(self):
        plan_config_id = request.args.get("plan_config_id")
        data = request.get_json()
        plan = plan_schema.load(data)
        config = requests.get(
            f"{request.url_root}config/plan/{plan_config_id}").json()
        # policy_selection = [
        #     pol for pol in policy if pol['name'] == plan.product_code][0]

        try:
            # planIsValid = plan.validate(
            #     policy=policy_selection, config=config[0])
            pass
        except Exception as e:
            print(str(e))
            return {"error": str(e)}, 400

        try:
            plan.save_to_db()
            plan_id = plan.plan_id
            session[plan_id] = {
                "plan": plan_schema.dump(plan),
                "plan_config": config,
                "policy": {}
            }
        except Exception as e:
            print(e)

        return plan_schema.dump(plan), 201
