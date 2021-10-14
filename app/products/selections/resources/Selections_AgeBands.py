from flask import request, session
from flask_restful import Resource

from ..models.AgeBandsModel import AgeBandsModel
from ..schemas.AgeBandsSchema import AgeBandsSchema

age_bands_list_schema = AgeBandsSchema(many=True)


class AgeBandsSelections(Resource):

    @classmethod
    def get(cls):
        plan_id = request.args.get("plan_id")
        plan_config_id = request.args.get("plan_config_id")
        # if a new plan request
        if plan_id is None:
            raise Exception("Please provide a plan ID query parameter")

        # if data exists in session
        session_data = session.get(int(plan_id))
        if session_data:
            return session_data

        # if looking up a plan not in session
        age_bands = AgeBandsModel.find_by_plan_id(plan_id)
        benefits = BenefitModel.find_benefits(plan_id)
        plan = PlanModel.find_by_id(plan_id)
        config = requests.get(
            f"{request.url_root}config/plan/{plan_config_id}").json()

        return {
            "plan": plan_schema.dump(plan),
            "plan_config": config,
            "benefits": benefit_list_schema.dump(benefits),
            "age_bands": age_bands_list_schema.dump(age_bands)
        }, 200

    def post(self):

        data = request.get_json()
        plan_id = data.get("plan_id")
        age_bands_data = data['age_bands']
        session_data = session.get(int(plan_id))

        age_bands = age_bands_list_schema.load(
            [{**band, "plan_id": plan_id} for band in age_bands_data])
        try:
            # AgeBandsModel.delete_by_plan_id(plan_id)
            AgeBandsModel.save_all_to_db(age_bands, plan_id)
            session[int(plan_id)] = {
                **session_data, "age_bands": age_bands_list_schema.dump(age_bands)}
        except Exception as e:
            print(e)

        return age_bands_list_schema.dump(age_bands), 201
