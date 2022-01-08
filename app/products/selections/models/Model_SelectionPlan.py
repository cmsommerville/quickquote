from app.extensions import db
from app.shared import BaseModel
from sqlalchemy import cast 
from sqlalchemy.ext.hybrid import hybrid_property

from ...__constants__ import TBL_NAMES
from ..utils.helpers import stateValidator

CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PRODUCT_VARIATION = TBL_NAMES['CONFIG_PRODUCT_VARIATIONS']
REF_STATE = TBL_NAMES['REF_STATE']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']


class Model_SelectionPlan(BaseModel):
    __tablename__ = SELECTION_PLAN

    selection_plan_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(f'{CONFIG_PRODUCT}.product_id'), nullable=False)
    config_product_variation_id = db.Column(db.ForeignKey(f'{CONFIG_PRODUCT_VARIATION}.product_variation_id'), nullable=False)
    config_state_id = db.Column(db.ForeignKey(f'{REF_STATE}.state_id'), nullable=False)
    plan_effective_date = db.Column(db.Date, nullable=False)
    plan_status = db.Column(db.String(50), default="Quoted")
    plan_name = db.Column(db.String(100))
    is_template_indicator = db.Column(db.String(1), default="N")
    cloned_plan_id = db.Column(db.Integer, db.ForeignKey(f'{SELECTION_PLAN}.selection_plan_id'))
    group_id = db.Column(db.Integer)
    broker_id = db.Column(db.Integer)

    cloned_plan = db.relationship("Model_SelectionPlan", remote_side=[selection_plan_id])
    benefits = db.relationship("Model_SelectionBenefit", back_populates="plan")
    provisions = db.relationship("Model_SelectionProvision", back_populates="plan")
    age_bands = db.relationship("Model_SelectionAgeBands", back_populates="plan")
    state = db.relationship("Model_RefStates")
    product_variation = db.relationship("Model_ConfigProductVariation")

    @hybrid_property
    def state_code(self):
        return self.state.state_code

    @hybrid_property
    def product_variation_code(self): 
        return self.product_variation.product_variation_code

        

    @classmethod
    def search_by_id(cls, id):
        return cls.query.filter(cast(cls.selection_plan_id, db.String).contains(str(id))).limit(10).all()

    def validate(self, policy: dict, config: dict) -> bool:
        """
        Validate the plan
        """
        configIsValid = stateValidator(self.rating_state,
                                       self.plan_effective_date,
                                       config['states'])

        policyIsValid = stateValidator(self.rating_state,
                                       self.plan_effective_date,
                                       policy['states'])

        return configIsValid and policyIsValid
