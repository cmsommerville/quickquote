from flask import request, session
from flask_restful import Resource
from app.models import mongo

from app.models.PlanRateModel import PlanRateModel
from app.models.FactorModel import FactorModel
from app.schemas.FactorSchema import FactorSchema
from app.rater import FactorGroupSize, FactorPrex

factor_list_schema = FactorSchema(many=True)


class FactorCalculator(Resource):

    @classmethod
    def post(cls):
        factorList = []
        plan_id = request.args.get("plan_id")
        if plan_id is None:
            raise Exception("Plan ID not provided")

        plan_rates = PlanRateModel.find_by_plan_id(plan_id)
        config = mongo.db.products.find_one(
            {"name": plan_rates[0].plan.product_name}, {"factors": True})

        factor_config = {
            obj['name']: obj
            for obj in config['factors']
        }

        for plan_rate in plan_rates:

            # instantiate factor calculation models with plan data
            factorGroupSize = FactorGroupSize(
                plan_rate, factor_config['groupsize'])
            factorPrex = FactorPrex(plan_rate, factor_config['prex'])

            # add factors to a list
            factorList = [factorGroupSize, factorPrex]

            # dump factors to JSON
            factor_data = factor_list_schema.dump(factorList)

            # save factor calculation data to DB
            FactorModel.save_all_to_db([FactorModel(**factor)
                                       for factor in factor_data])

        return factor_data, 201
