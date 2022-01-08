from sqlalchemy.orm import aliased, contains_eager, Query
from sqlalchemy import and_, between
from app.extensions import db

from ..config.models import Model_ConfigProduct, Model_ConfigFactor, \
    Model_ConfigFactorRule, Model_ConfigProvision
from ..selections.models import Model_SelectionPlan, Model_SelectionProvision

def query_config_factors(plan: Model_SelectionPlan) -> Query: 
    plan_id = plan.selection_plan_id

    # base query
    qry = db.session.query(Model_SelectionProvision)

    # filter on selected plan
    qry = qry.filter(
            Model_SelectionProvision.selection_plan_id == plan.selection_plan_id
        )

    # join to configured factors
    qry = qry.join(Model_ConfigProvision)
    
    # join to configured factors
    qry = qry.join(Model_ConfigFactor)

    # join to configured factor rules
    qry = qry.join(Model_ConfigFactorRule)


    return qry.options(
        contains_eager(Model_SelectionProvision.config_provision, 
            Model_ConfigProvision.factors, 
            Model_ConfigFactor.factor_rules))

