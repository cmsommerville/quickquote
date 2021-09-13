from app.extensions import db
import datetime

from .ProvisionModel import ProvisionModel
from .CoverageModel import CoverageModel
from .BenefitModel import BenefitModel


class PlanModel(db.Model):
    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(50), nullable=False)
    rating_state = db.Column(db.String(2), nullable=False)
    plan_effective_date = db.Column(db.Date, nullable=False)
    plan_status = db.Column(db.String(50), default="Quoted")

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    coverages = db.relationship("CoverageModel", back_populates="plan")
    benefits = db.relationship("BenefitModel", back_populates="plan")
    provisions = db.relationship("ProvisionModel", back_populates="plan")

    def __repr__(self):
        return f"<Plan Id: {self.plan_id} -- Product Name: `{self.product_code}`>"

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
