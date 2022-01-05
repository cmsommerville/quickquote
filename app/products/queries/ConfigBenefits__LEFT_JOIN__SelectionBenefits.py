from sqlalchemy.orm import aliased, contains_eager, Query
from sqlalchemy import and_, between
from app.extensions import db

from ..config.models import Model_ConfigBenefitProductVariation, Model_ConfigBenefit, Model_ConfigBenefitDuration, Model_ConfigBenefitDurationItem
from ..selections.models import Model_SelectionBenefit, Model_SelectionBenefitDuration, Model_SelectionPlan

def query_benefits(plan: Model_SelectionPlan) -> Query: 
    plan_id = plan.selection_plan_id

    # alias the benefit states records
    ConfigBenefitState = aliased(Model_ConfigBenefit)

    # base query
    bnft_prod_variation = db.session.query(Model_ConfigBenefitProductVariation)

    # join to benefit config
    bnft_prod_variation = bnft_prod_variation.join(Model_ConfigBenefit)

    # join to state specific benefit config
    bnft_prod_variation = bnft_prod_variation.join(
        ConfigBenefitState, and_(
            ConfigBenefitState.parent_id == Model_ConfigBenefit.benefit_id
        ))

    # outer join to duration config
    bnft_prod_variation = bnft_prod_variation.outerjoin(Model_ConfigBenefitDuration, 
            Model_ConfigBenefit.benefit_id == Model_ConfigBenefitDuration.benefit_id
        )

    # outer join to duration items config
    bnft_prod_variation = bnft_prod_variation.outerjoin(Model_ConfigBenefitDurationItem)

    # main filter 
    #   - product variation
    #   - master benefit must be effective on plan effective date
    #   - benefit must be effective in the situs state on the plan effective date
    #   - exclude the parent benefit record
    #   - select the state specific benefit record
    bnft_prod_variation = bnft_prod_variation.filter(
            Model_ConfigBenefitProductVariation.product_variation_id == plan.config_product_variation_id, 
            between(
                plan.plan_effective_date, 
                Model_ConfigBenefit.benefit_effective_date, 
                Model_ConfigBenefit.benefit_expiration_date), 
            between(
                plan.plan_effective_date, 
                ConfigBenefitState.benefit_effective_date, 
                ConfigBenefitState.benefit_expiration_date), 
            Model_ConfigBenefit.parent_id == None, 
            ConfigBenefitState.state_id == plan.config_state_id
        )

    # left join the selected benefits
    bnft_prod_variation = bnft_prod_variation.outerjoin(Model_SelectionBenefit, and_(
            Model_ConfigBenefit.benefit_id == Model_SelectionBenefit.config_benefit_id,
            Model_SelectionBenefit.selection_plan_id == plan_id, 
        ))

    # left join the selected benefit durations
    bnft_prod_variation = bnft_prod_variation.outerjoin(Model_SelectionBenefitDuration, and_(
            Model_ConfigBenefitDuration.benefit_duration_id == Model_SelectionBenefitDuration.config_benefit_duration_id, 
            Model_SelectionBenefitDuration.selection_plan_id == plan_id, 
        ))

    # make sure that the relationships are filtered with contains_eager
    bnft_prod_variation = bnft_prod_variation.options(
            contains_eager(
                Model_ConfigBenefitProductVariation.benefit, 
                Model_ConfigBenefit.selected_benefit
            ), 
            contains_eager(
                Model_ConfigBenefitProductVariation.benefit,
                Model_ConfigBenefit.durations,
                Model_ConfigBenefitDuration.selected_duration_item
            )
        )

    return bnft_prod_variation

