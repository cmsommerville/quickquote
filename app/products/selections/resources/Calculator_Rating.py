from flask import request
from flask_restful import Resource

from ..classes import Rater, RatingCalculator
from ..models import PlanModel, BenefitModel, ProvisionModel, BenefitRateModel
from ..schemas import BenefitRateSchema, PremiumByBenefitAgeBandRateSchema

benefit_rate_list_schema = BenefitRateSchema(many=True)
premium_by_benefit_age_band_rate_list_schema = PremiumByBenefitAgeBandRateSchema(
    many=True)


class RatingCalculatorResource(Resource):

    @classmethod
    def get(cls):
        plan_id = request.args.get("plan_id")
        if plan_id is None:
            raise Exception("Please provide a plan_id query parameter")

        benefits = BenefitModel.find_benefits(plan_id)
        coverages = [benefit.coverage for benefit in benefits]
        plan = benefits[0].plan
        provisions = ProvisionModel.find_plan_provisions(plan_id)

        rater = RatingCalculator(
            plan=plan, provisions=provisions, coverages=coverages, benefits=benefits)

        benefit_rates = rater.execute()
        return premium_by_benefit_age_band_rate_list_schema.dump(benefit_rates), 200

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
