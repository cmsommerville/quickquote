from app.models import db
import datetime


class FactorModel(db.Model):
    __tablename__ = "factors"

    factor_id = db.Column(db.Integer, primary_key=True)
    plan_rate_id = db.Column(
        db.Integer, db.ForeignKey('plan_rates.plan_rate_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    provision_id = db.Column(
        db.Integer, db.ForeignKey('provisions.provision_id'))
    factor_type = db.Column(db.String(10), nullable=False)
    factor_name = db.Column(db.String(50), nullable=False)
    factor_selection = db.Column(db.String(36), nullable=False)
    factor_selection_type = db.Column(db.String(10), nullable=False)
    factor_value = db.Column(db.Float, nullable=False)

    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(
        db.DateTime, default=datetime.datetime(9999, 12, 31, 0, 0, 0))
    active_record_indicator = db.Column(db.String(1), default='Y')

    plan_rate = db.relationship("PlanRateModel", back_populates="factors")

    def __repr__(self):
        return f"<Factor Id: {self.factor_id} -- Factor Name: `{self.factor_name}`>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.factor_id == id).first()

    @classmethod
    def find_plan_factors(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id, cls.active_record_indicator == 'Y').all()

    @classmethod
    def expire_factors(cls, plan_id):
        factors = cls.find_plan_factors(plan_id)
        if factors:
            for factor in factors:
                factor.row_exp_dts = db.func.current_timestamp()
                factor.active_record_indicator = 'N'
                db.session.add(factor)

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
            cls.expire_factors(plan_id)
            for factor in factors:
                db.session.add(factor)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
