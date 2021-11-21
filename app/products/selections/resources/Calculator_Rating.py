import os
from flask import request, session
from flask_restful import Resource

from ..classes import Rating_Main
from ..models import BenefitRateModel, BenefitAgeRateModel, BenefitFactorModel

from ..schemas import PlanSchema, BenefitSchema, ProvisionSchema, \
    AgeBandsSchema, BenefitRateSchema, PremiumByPlanRateSchema, \
    PlanRateSchema

from app.data.policy import policy

# PRODUCT_CODE = os.getenv("PRODUCT_CODE")
# PRODUCT_VARIATION_CODE = os.getenv("PRODUCT_VARIATION_CODE")


benefit_list_schema = BenefitSchema(many=True)
plan_schema = PlanSchema()
provision_list_schema = ProvisionSchema(many=True)
age_bands_list_schema = AgeBandsSchema(many=True)
benefit_rate_list_schema = BenefitRateSchema(many=True)
premium_by_plan_rate_list_schema = PremiumByPlanRateSchema(
    many=True)


class RatingCalculatorResource(Resource):

    @classmethod
    def get(cls):
        return "success", 200

    @classmethod
    def post(cls):
        plan_id = request.args.get("plan_id")
        if plan_id is None:
            raise Exception("Please provide a plan_id query parameter")
        BenefitFactorModel.delete_by_plan_id(plan_id)
        BenefitAgeRateModel.delete_by_plan_id(plan_id)
        BenefitRateModel.delete_by_plan_id(plan_id)

        session_data = session.get(int(plan_id))

        plan = plan_schema.load(session_data['plan'])
        plan_config = session_data['plan_config']
        age_bands = age_bands_list_schema.load(session_data['age_bands'])
        provisions = provision_list_schema.load(session_data['provisions'])
        benefits = benefit_list_schema.load(session_data['benefits'])

        # applicable_policy = [
        #     p for p in policy if p['name'] == plan.product_code][0]

        rater = Rating_Main(
            plan=plan,
            config=plan_config,
            provisions=provisions,
            age_bands=age_bands,
            benefits=benefits,
            product_code=plan.product_code,
            product_variation_code=plan.product_variation_code,
            policy=None
        )
        plan_rates = rater.calculate()

        return premium_by_plan_rate_list_schema.dump(plan_rates), 200
