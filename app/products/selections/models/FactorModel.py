from app.extensions import db
import datetime


class FactorModel(db.Model):
    __tablename__ = "factors"

    factor_id = db.Column(db.Integer, primary_key=True)
    benefit_rate_id = db.Column(
        db.Integer, db.ForeignKey('benefit_rates.benefit_rate_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    provision_id = db.Column(
        db.Integer, db.ForeignKey('provisions.provision_id'))
    factor_type = db.Column(db.String(10), nullable=False)
    factor_name = db.Column(db.String(50), nullable=False)
    factor_selection = db.Column(db.String(36), nullable=False)
    factor_selection_type = db.Column(db.String(10), nullable=False)
    factor_value = db.Column(db.Float, nullable=False)

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    benefit_rate = db.relationship(
        "BenefitRateModel", back_populates="factors")

    def __repr__(self):
        return f"<Factor Id: {self.factor_id} -- Factor Name: `{self.factor_name}`>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.factor_id == id).first()

    @classmethod
    def find_plan_factors(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id).all()

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
        else:
            db.session.commit()

    @classmethod
    def save_all_to_db(cls, factors, plan_id):
        try:
            for factor in factors:
                db.session.add(factor)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    @classmethod
    def delete_by_benefit_rate_id(cls, benefit_rate_id, commit=True):
        try:
            cls.query.filter(cls.benefit_rate_id == benefit_rate_id).delete()
        except:
            db.session.rollback()
            raise
        else:
            if commit:
                db.session.commit()
