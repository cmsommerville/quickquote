from flask import request, session
from flask_restful import Resource

from ..classes import Rating_PremiumCalculator
from ..models import PlanModel, BenefitModel, ProvisionModel, AgeBandsModel, \
    BenefitRateModel, BenefitAgeRateModel, BenefitFactorModel

from ..schemas import PlanSchema, BenefitSchema, ProvisionSchema,  AgeBandsSchema, BenefitRateSchema, PremiumByBenefitAgeBandRateSchema

benefit_list_schema = BenefitSchema(many=True)
plan_schema = PlanSchema()
provision_list_schema = ProvisionSchema(many=True)
age_bands_list_schema = AgeBandsSchema(many=True)
benefit_rate_list_schema = BenefitRateSchema(many=True)
premium_by_benefit_age_band_rate_list_schema = PremiumByBenefitAgeBandRateSchema(
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
        plan_config = session_data['plan_config'][0]
        age_bands = age_bands_list_schema.load(session_data['age_bands'])
        provisions = provision_list_schema.load(session_data['provisions'])
        benefits = benefit_list_schema.load(session_data['benefits'])

        rater = Rating_PremiumCalculator(
            plan=plan,
            plan_config=plan_config,
            provisions=provisions,
            age_bands=age_bands,
            benefits=benefits
        )
        benefit_rates = rater.calculate()

        return premium_by_benefit_age_band_rate_list_schema.dump(benefit_rates), 200
