from app.models import db


class FactorModel(db.Model):
    __tablename__ = "factors"

    factor_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.plan_id'))
    factor_type = db.Column(db.String(10), nullable=False)
    factor_name = db.Column(db.String(50), nullable=False)
    factor_selection = db.Column(db.String(100), nullable=False)
    factor_value = db.Column(db.Float, nullable=False)

    plan = db.relationship("PlanModel", back_populates="factors")
