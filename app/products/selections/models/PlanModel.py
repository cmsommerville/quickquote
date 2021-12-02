from app.extensions import db
from app.shared import BaseModel
import datetime
from sqlalchemy import cast

from .ProvisionModel import ProvisionModel
from .CoverageModel import CoverageModel
from .BenefitModel import BenefitModel
from .AgeBandsModel import AgeBandsModel

from ..utils.helpers import stateValidator


class PlanModel(BaseModel):
    __tablename__ = "selections_plans"

    plan_id = db.Column(db.Integer, primary_key=True)
    plan_number = db.Column(db.Integer, db.Sequence('seq_plans__plan_number'))
    product_code = db.Column(db.String(50), nullable=False)
    product_variation_code = db.Column(db.String(50), nullable=False)
    rating_state = db.Column(db.String(2), nullable=False)
    plan_effective_date = db.Column(db.Date, nullable=False)
    plan_status = db.Column(db.String(50), default="Quoted")
    plan_config_id = db.Column(db.String(36), nullable=False)
    plan_name = db.Column(db.String(100))
    is_template_indicator = db.Column(db.String(1), default="N")
    cloned_plan_id = db.Column(db.Integer, db.ForeignKey('selections_plans.plan_id'))

    cloned_plan = db.relationship("PlanModel", remote_side=[plan_id])
    coverages = db.relationship("CoverageModel", back_populates="plan")
    benefits = db.relationship("BenefitModel", back_populates="plan")
    provisions = db.relationship("ProvisionModel", back_populates="plan")
    age_bands = db.relationship("AgeBandsModel", back_populates="plan")

    def __repr__(self):
        return f"<Plan Id: {self.plan_id} -- Product Name: `{self.product_code}`>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.plan_id == id).first()

    @classmethod
    def search_by_id(cls, id):
        return cls.query.filter(cast(cls.plan_id, db.String).contains(str(id))).limit(10).all()

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
