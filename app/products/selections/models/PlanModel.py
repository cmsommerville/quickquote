from app.extensions import db
from app.shared import VersionedTable
import datetime
from sqlalchemy import cast

from .ProvisionModel import ProvisionModel
from .CoverageModel import CoverageModel
from .BenefitModel import BenefitModel
from .AgeBandsModel import AgeBandsModel

from ..utils.helpers import stateValidator


class PlanModel(db.Model, VersionedTable):
    __tablename__ = "plans"

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
    cloned_plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))

    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(db.DateTime, default='9999-12-31 00:00:00.000')
    active_record_indicator = db.Column(db.String(1), default='Y')
    created_by = db.Column(db.String(50), default="cmsommerville")

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    cloned_plan = db.relationship("PlanModel", remote_side=[plan_id])
    coverages = db.relationship("CoverageModel", back_populates="plan",
                                primaryjoin="and_(PlanModel.plan_id == CoverageModel.plan_id, CoverageModel.active_record_indicator == 'Y')")
    benefits = db.relationship("BenefitModel", back_populates="plan",
                               primaryjoin="and_(PlanModel.plan_id == BenefitModel.plan_id, BenefitModel.active_record_indicator == 'Y')")
    provisions = db.relationship("ProvisionModel", back_populates="plan",
                                 primaryjoin="and_(PlanModel.plan_id == ProvisionModel.plan_id, ProvisionModel.active_record_indicator == 'Y')")
    age_bands = db.relationship("AgeBandsModel", back_populates="plan",
                                primaryjoin="and_(PlanModel.plan_id == AgeBandsModel.plan_id, AgeBandsModel.active_record_indicator == 'Y')")

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

    def save_to_db(self):
        try:
            if self.plan_number:
                db.session.query(PlanModel).filter(
                    PlanModel.plan_number == self.plan_number,
                    PlanModel.active_record_indicator == 'Y').update({
                        PlanModel.active_record_indicator: "N",
                        PlanModel.row_exp_dts: db.func.current_timestamp()
                    })

            db.session.add(self)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
