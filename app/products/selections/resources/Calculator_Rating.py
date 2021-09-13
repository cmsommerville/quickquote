from flask import request
from flask_restful import Resource

from ..classes import Rater
from ..models import PlanModel, BenefitModel, ProvisionModel, PlanRatingAttributeModel, BenefitRateModel
from ..schemas import BenefitRateSchema

benefit_rate_list_schema = BenefitRateSchema(many=True)


class RatingCalculator(Resource):

    @classmethod
    def get(cls):
        plan_id = request.args.get("plan_id")
        if plan_id is None:
            raise Exception("Please provide a plan_id query parameter")

        benefits = BenefitModel.find_benefits(plan_id)
        coverages = [benefit.coverage for benefit in benefits]
        plan = benefits[0].plan
        provisions = ProvisionModel.find_plan_provisions(plan_id)
        plan_rating_attributes = PlanRatingAttributeModel.find_plan_rating_attributes(
            plan_id)

        rater = Rater(plan=plan, provisions=provisions, coverages=coverages,
                      benefits=benefits, plan_rating_attributes=plan_rating_attributes)

        benefit_rates = rater.execute()
        return benefit_rate_list_schema.dump(benefit_rates), 200

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
