from flask import request, session
from flask_restful import Resource

from ..models.AgeBandsModel import AgeBandsModel
from ..schemas.AgeBandsSchema import AgeBandsSchema

age_bands_list_schema = AgeBandsSchema(many=True)


class AgeBandsSelections(Resource):

    @classmethod
    def get(cls):
        plan_id = request.args.get("plan_id")
        if plan_id is None:
            raise Exception("Please provide a plan_id query parameter")

        plan = AgeBandsModel.find_by_plan_id(plan_id)
        return age_bands_list_schema.dump(plan), 200

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
