from ..schemas import *


def BenefitAmountReducer(
        config: Config_BenefitAmountsSchema,
        policy: Policy_BenefitAmountsSchema) -> Config_BenefitAmountsSchema:

    return {
        **config, **policy,
        "min": max([config.get('min'), policy.get('min')]),
        "max": min([config.get('max'), policy.get('max')]),
    }
