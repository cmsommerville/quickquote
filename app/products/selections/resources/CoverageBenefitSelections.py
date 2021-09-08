from flask import request
from flask_restful import Resource

from ..models.BenefitModel import BenefitModel
from ..models.CoverageModel import CoverageModel

from ..schemas.BenefitSchema import BenefitSchema
from ..schemas.CoverageSchema import CoverageSchema

benefit_schema = BenefitSchema()
benefit_list_schema = BenefitSchema(many=True)
coverage_schema = CoverageSchema()
coverage_list_schema = CoverageSchema(many=True)

benefit_keys = [k for k, v in benefit_schema.fields.items()]
coverage_keys = [k for k, v in coverage_schema.fields.items()]


class CoverageBenefitSelections(Resource):

    @classmethod
    def get(cls):
        plan_id = request.args.get("plan_id")
        if plan_id is None:
            raise Exception("Please provide a plan_id query parameter")

        benefits = BenefitModel.find_benefits(plan_id)
        return benefit_list_schema.dump(benefits), 200

    @classmethod
    def post(cls):
        coverage_dict = {}
        data = request.get_json()
        try:
            plan_id = data[0]["plan_id"]
        except Exception as e:
            return str(e), 400

        for item in data:
            coverage_code = item['coverage_code']
            if coverage_dict.get(coverage_code) is None:
                coverage_dict[coverage_code] = CoverageModel(
                    plan_id=plan_id, coverage_code=coverage_code)

            benefit = benefit_schema.load(
                {k: v for k, v in item.items() if k in benefit_keys})
            coverage_dict[coverage_code].benefits.append(benefit)

        try:
            coverages = [v for k, v in coverage_dict.items()]
            CoverageModel.save_all_to_db(coverages, plan_id)
        except Exception as e:
            return str(e), 400

        return "created", 201
