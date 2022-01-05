from sqlalchemy.orm import aliased, contains_eager, Query
from sqlalchemy import and_, between
from app.extensions import db

from ..config.models import Model_ConfigProduct, Model_ConfigProvision, \
    Model_ConfigProvisionStateAvailability
from ..selections.models import Model_SelectionPlan, Model_SelectionProvision

def query_config_provisions(plan: Model_SelectionPlan) -> Query: 
    plan_id = plan.selection_plan_id

    # base query
    qry = db.session.query(Model_ConfigProvision)

    # join to age bands
    qry = qry.join(Model_ConfigProvisionStateAvailability)

    # filter on state
    qry = qry.filter(
            Model_ConfigProvisionStateAvailability.state_id == plan.config_state_id, 
            between(
                plan.plan_effective_date, 
                Model_ConfigProvision.provision_effective_date, 
                Model_ConfigProvision.provision_expiration_date),
            between(
                plan.plan_effective_date, 
                Model_ConfigProvisionStateAvailability.state_effective_date, 
                Model_ConfigProvisionStateAvailability.state_expiration_date)
        )

    return qry.options(
        contains_eager(Model_ConfigProvision.states), 
        contains_eager(Model_ConfigProvision.ui_component))


def query_selection_provisions(plan: Model_SelectionPlan) -> Query:
    plan_id = plan.selection_plan_id
    qry = query_config_provisions(plan)

    # inner join to get selected provisions
    qry = qry.join(Model_SelectionProvision)

    # filter for plan specific provisions
    qry = qry.filter(Model_SelectionProvision.selection_plan_id == plan_id)
    
    return qry.options(
        contains_eager(Model_ConfigProvision.selected_provision))