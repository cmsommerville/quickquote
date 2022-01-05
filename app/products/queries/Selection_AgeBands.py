from sqlalchemy.orm import aliased, contains_eager, Query
from sqlalchemy import and_, between
from app.extensions import db

from ..config.models import Model_ConfigAgeBandSet, Model_ConfigAgeBand
from ..selections.models import Model_SelectionAgeBands, Model_SelectionPlan

def query_config_benefits(plan: Model_SelectionPlan) -> Query: 
    plan_id = plan.selection_plan_id

    # base query
    qry = db.session.query(Model_ConfigAgeBandSet)

    # join to age bands
    qry = qry.join(Model_ConfigAgeBand)

    # filter on product variation and state, but not effective date YET
    state_qry = qry.filter(
            Model_ConfigAgeBandSet.product_variation_id == plan.config_product_variation_id, 
            Model_ConfigAgeBandSet.state_id == plan.config_state_id
        )

    # if age bands are defined by state, then check that the age bands are effective
    if state_qry.count() > 0:
        state_qry = state_qry.filter(
            between(
                plan.plan_effective_date, 
                Model_ConfigAgeBandSet.age_band_effective_date, 
                Model_ConfigAgeBandSet.age_band_expiration_date)
            )
        return state_qry.options(contains_eager(Model_ConfigAgeBandSet.age_bands))

    ##########################################
    #   ONLY CONTINUE IF NO STATES MATCH

    # query for all states option
    qry = qry.filter(
            Model_ConfigAgeBandSet.product_variation_id == plan.config_product_variation_id, 
            Model_ConfigAgeBandSet.state_id == 0, 
            between(
                plan.plan_effective_date, 
                Model_ConfigAgeBandSet.age_band_effective_date, 
                Model_ConfigAgeBandSet.age_band_expiration_date)
        )

    return state_qry.options(contains_eager(Model_ConfigAgeBandSet.age_bands))
