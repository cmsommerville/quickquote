from app.extensions import db
import datetime

from .ProvisionModel import ProvisionModel
from .CoverageModel import CoverageModel
from .BenefitModel import BenefitModel
from .AgeBandsModel import AgeBandsModel


class PlanModel(db.Model):
    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, primary_key=True)
    plan_number = db.Column(db.Integer, db.Sequence('seq_plans__plan_number'))
    product_code = db.Column(db.String(50), nullable=False)
    product_variation_code = db.Column(db.String(50), nullable=False)
    rating_state = db.Column(db.String(2), nullable=False)
    plan_effective_date = db.Column(db.Date, nullable=False)
    plan_status = db.Column(db.String(50), default="Quoted")

    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(db.DateTime, default='9999-12-31 00:00:00.000')
    active_record_indicator = db.Column(db.String(1), default='Y')

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    coverages = db.relationship("CoverageModel", back_populates="plan")
    benefits = db.relationship("BenefitModel", back_populates="plan")
    provisions = db.relationship("ProvisionModel", back_populates="plan")
    age_bands = db.relationship("AgeBandsModel", back_populates="plan")

    def __repr__(self):
        return f"<Plan Id: {self.plan_id} -- Product Name: `{self.product_code}`>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.plan_id == id).first()

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
