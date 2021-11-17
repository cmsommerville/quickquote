import requests
from flask import request, session
from flask_restful import Resource

from ..models.PlanModel import PlanModel
from ..models.BenefitModel import BenefitModel
from ..models.CoverageModel import CoverageModel

from ..schemas.PlanSchema import PlanSchema
from ..schemas.BenefitSchema import BenefitSchema
from ..schemas.CoverageSchema import CoverageSchema

benefit_schema = BenefitSchema()
benefit_list_schema = BenefitSchema(many=True)
coverage_schema = CoverageSchema()
coverage_list_schema = CoverageSchema(many=True)
plan_schema = PlanSchema()

benefit_keys = [k for k, v in benefit_schema.fields.items()]
coverage_keys = [k for k, v in coverage_schema.fields.items()]


class CoverageBenefitSelections(Resource):

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
        benefits = BenefitModel.find_benefits(plan_id)
        plan = PlanModel.find_by_id(plan_id)
        config = requests.get(
            f"{request.url_root}config/plan/{plan_config_id}").json()

        return {
            "plan": plan_schema.dump(plan),
            "plan_config": config,
            "benefits": benefit_list_schema.dump(benefits)
        }, 200

    @classmethod
    def post(cls):
        coverage_dict = {}
        benefits_list = []
        data = request.get_json()

        try:
            plan_id = data[0]["plan_id"]
        except Exception as e:
            return str(e), 400

        session_data = session.get(int(plan_id))

        for item in data:
            coverage_code = item['coverage_code']
            if coverage_dict.get(coverage_code) is None:
                coverage_dict[coverage_code] = CoverageModel(
                    plan_id=plan_id, coverage_code=coverage_code)

            benefit = benefit_schema.load(
                {k: v for k, v in item.items() if k in benefit_keys})

            benefit.validate()
            coverage_dict[coverage_code].benefits.append(benefit)
            benefits_list.append(benefit)

        try:
            coverages = [v for k, v in coverage_dict.items()]
            CoverageModel.save_all_to_db(coverages, plan_id)
        except Exception as e:
            return str(e), 400

        try:
            session[int(plan_id)] = {**session_data,
                                     "benefits": benefit_list_schema.dump(benefits_list)}
        except Exception as e:
            return str(e), 400

        return "created", 201
