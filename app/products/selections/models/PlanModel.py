from app.extensions import db
import datetime

from .ProvisionModel import ProvisionModel
from .CoverageModel import CoverageModel
from .BenefitModel import BenefitModel
from .PlanRatingAttributeModel import PlanRatingAttributeModel


class PlanModel(db.Model):
    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, primary_key=True)
    plan_number = db.Column(db.Integer, db.Sequence('seq_plans__plan_number'))
    product_code = db.Column(db.String(50), nullable=False)
    rating_state = db.Column(db.String(2), nullable=False)
    plan_effective_date = db.Column(db.Date, nullable=False)
    plan_status = db.Column(db.String(50), default="Quoted")

    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(
        db.DateTime, default=datetime.datetime(9999, 12, 31, 0, 0, 0))
    active_record_indicator = db.Column(db.String(1), default="Y")

    coverages = db.relationship("CoverageModel", back_populates="plan",
                                primaryjoin="and_(PlanModel.plan_id == CoverageModel.plan_id, CoverageModel.active_record_indicator=='Y')")
    benefits = db.relationship("BenefitModel", back_populates="plan",
                               primaryjoin="and_(PlanModel.plan_id == BenefitModel.plan_id, BenefitModel.active_record_indicator=='Y')")
    provisions = db.relationship("ProvisionModel", back_populates="plan",
                                 primaryjoin="and_(PlanModel.plan_id == ProvisionModel.plan_id, ProvisionModel.active_record_indicator=='Y')")
    plan_rating_attributes = db.relationship(
        "PlanRatingAttributeModel", back_populates="plan")

    def __repr__(self):
        return f"<Plan Id: {self.plan_id} -- Product Name: `{self.product_name}`>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.plan_id == id).first()

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
