from flask import request, session
from flask_restful import Resource

from app.models.PlanModel import PlanModel
from app.models.FactorModel import FactorModel
from app.schemas.FactorSchema import FactorSchema
from app.rater import FactorGroupSize, FactorPrex

factor_list_schema = FactorSchema(many=True)


class FactorCalculator(Resource):

    @classmethod
    def get(cls):
        factorList = []
        plan_id = request.args.get("plan_id")
        if plan_id is None:
            raise Exception("Plan ID not provided")

        plan = PlanModel.find_by_id(plan_id)

        # instantiate factor calculation models with plan data
        factorGroupSize = FactorGroupSize(plan)
        factorPrex = FactorPrex(plan)

        # add factors to a list
        factorList = [factorGroupSize, factorPrex]

        # dump factors to JSON
        factor_data = factor_list_schema.dump(factorList)

        # save factor calculation data to DB
        FactorModel.save_all_to_db([FactorModel(**factor)
                                   for factor in factor_data])

        return factor_data, 201
