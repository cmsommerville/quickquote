from flask import request, session
from flask_restful import Resource
from app.models import mongo

from app.models.PlanRateModel import PlanRateModel
from app.models.FactorModel import FactorModel
from app.schemas.FactorSchema import FactorSchema
from app.rater import FactorGroupSize, FactorPrex, FactorReductionAt70, FactorAttributesBase

factor_list_schema = FactorSchema(many=True)


factor_classes = {
    'groupsize': FactorGroupSize,
    'prex': FactorPrex,
    'reductionAt70': FactorReductionAt70
}


class FactorCalculator(Resource):

    @classmethod
    def post(cls):
        factorList = []
        plan_id = request.args.get("plan_id")
        if plan_id is None:
            raise Exception("Plan ID not provided")

        # get all the objects for factor calculation
        plan_rates = PlanRateModel.find_by_plan_id(plan_id)
        plan = plan_rates[0].plan
        provisions = plan.provisions
        group = plan.group

        # get provision configuration from mongo
        provisions_config = mongo.db.products.find_one(
            {"name": plan_rates[0].plan.product_name}, {"provisions": True})['provisions']

        # create a dictionary of all the factor types
        provisions_dict = {
            provision.provision_code: provision
            for provision in provisions
        }

        # loop over plan rates
        for plan_rate in plan_rates:

            # loop over each provision in the configuration
            for prov_config in provisions_config:
                provision_name = prov_config['name']
                factor_config = prov_config.get('factor')
                # flatten all rating attributes into factor attributes object
                factor_attributes = FactorAttributesBase(group, plan, plan_rate,
                                                         provisions_dict.get(provision_name))

                # get the setter object and instantiate with factor attributes
                factor_instance = factor_classes[provision_name](
                    factor_attributes, factor_config)

                # add factors to a list
                factorList.append(factor_instance)

        # dump factors to JSON
        factor_data = factor_list_schema.dump(factorList)

        # save factor calculation data to DB
        FactorModel.save_all_to_db([FactorModel(**{**factor, "plan_id": plan_id})
                                    for factor in factor_data], plan_id)

        return factor_data, 201
