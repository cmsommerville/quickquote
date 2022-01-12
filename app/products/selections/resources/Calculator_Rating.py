import os
from flask import request, session
from flask_restful import Resource

from ..classes import Rating_Main
from ..models import Model_SelectionPlan

# from ..schemas import PlanSchema, BenefitSchema, ProvisionSchema, \
#     AgeBandsSchema, BenefitRateSchema, PremiumByPlanRateSchema, \
#     PlanRateSchema

# from app.data.policy import policy

# PRODUCT_CODE = os.getenv("PRODUCT_CODE")
# PRODUCT_VARIATION_CODE = os.getenv("PRODUCT_VARIATION_CODE")


# benefit_list_schema = BenefitSchema(many=True)
# plan_schema = PlanSchema()
# provision_list_schema = ProvisionSchema(many=True)
# age_bands_list_schema = AgeBandsSchema(many=True)
# benefit_rate_list_schema = BenefitRateSchema(many=True)
# premium_by_plan_rate_list_schema = PremiumByPlanRateSchema(
#     many=True)


class RatingCalculatorResource(Resource):

    @classmethod
    def get(cls):
        return "success", 200

    @classmethod
    def post(cls):
        plan_id = request.args.get("plan_id")
        if plan_id is None:
            raise Exception("Please provide a plan_id query parameter")

        plan = Model_SelectionPlan.find_one(plan_id)
        rater = Rating_Main(plan=plan)
        plan_rates = rater.calculate()

        return "woot", 200
        return premium_by_plan_rate_list_schema.dump(plan_rates), 200
