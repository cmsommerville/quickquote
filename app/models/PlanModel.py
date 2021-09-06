from app.models import db
import datetime

from app.models.ProvisionModel import ProvisionModel
from app.models.FactorModel import FactorModel
from app.models.PlanRateModel import PlanRateModel
from app.models.CoverageModel import CoverageModel
from app.models.BenefitModel import BenefitModel


class PlanModel(db.Model):
    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, primary_key=True)
    plan_number = db.Column(db.Integer, db.Sequence('seq_plans__plan_number'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))
    product_name = db.Column(db.String(50), nullable=False)
    rating_state = db.Column(db.String(2), nullable=False)
    plan_effective_date = db.Column(db.Date, nullable=False)
    plan_status = db.Column(db.String(50), default="Quoted")
    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(
        db.DateTime, default=datetime.datetime(9999, 12, 31, 0, 0, 0))
    active_record_indicator = db.Column(db.String(1), default="Y")

    group = db.relationship("GroupModel", back_populates="plans")
    # factors = db.relationship("FactorModel", back_populates="plan")
    plan_rates = db.relationship("PlanRateModel", back_populates="plan")
    coverages = db.relationship("CoverageModel", back_populates="plan")
    benefits = db.relationship("BenefitModel", back_populates="plan")
    provisions = db.relationship("ProvisionModel", back_populates="plan")

    def __repr__(self):
        return f"<Plan Id: {self.plan_id} -- Product Name: `{self.product_name}`>"

    # def reset(self, data):
    #     self.group_id = data.get("group_id", self.group_id)
    #     self.product_name = data.get("product_name", self.product_name)
    #     self.rating_state = data.get("rating_state", self.rating_state)
    #     if data.get("plan_effective_date"):
    #         self.plan_effective_date = datetime.datetime.strptime(
    #             data.get("plan_effective_date"), '%Y-%m-%d').date()

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
