from app.extensions import db
import datetime


class BenefitRateModel(db.Model):
    __tablename__ = "benefit_rates"

    benefit_rate_id = db.Column(db.Integer, primary_key=True)
    benefit_id = db.Column(db.Integer, db.ForeignKey('benefits.benefit_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    age = db.Column(db.Integer, nullable=False)
    family_code = db.Column(db.String(3), nullable=False)
    smoker_status = db.Column(db.String(1), nullable=False)
    benefit_rate_uuid = db.Column(db.String(36), nullable=False)
    benefit_rate_base_premium = db.Column(db.Numeric(12, 5), nullable=False)
    benefit_rate_factor = db.Column(db.Numeric(8, 5))
    benefit_rate_benefit_factor = db.Column(db.Numeric(8, 5))
    benefit_rate_final_premium = db.Column(db.Numeric(12, 5))
    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(
        db.DateTime, default=datetime.datetime(9999, 12, 31, 0, 0, 0))
    active_record_indicator = db.Column(db.String(1), default='Y')

    plan = db.relationship("PlanModel")
    benefit = db.relationship("BenefitModel", back_populates="benefit_rates")
    factors = db.relationship("FactorModel", back_populates="benefit_rate")

    def __repr__(self):
        return f"<Benefit Rate Id: {self.benefit_rate_id}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.benefit_rate_id == id).first()

    @classmethod
    def find_benefit_rates_by_plan(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id, cls.active_record_indicator == 'Y').options(db.joinedload(cls.benefit)).all()

    @classmethod
    def find_benefit_rates_by_benefit(cls, benefit_id):
        return cls.query.filter(cls.benefit_id == benefit_id, cls.active_record_indicator == 'Y').options(db.joinedload(cls.benefit)).all()

    @classmethod
    def expire_by_benefit(cls, benefit_id):
        benefit_rates = cls.find_benefit_rates_by_benefit(benefit_id)
        if benefit_rates:
            for benefit_rate in benefit_rates:
                benefit_rate.row_exp_dts = db.func.current_timestamp()
                benefit_rate.active_record_indicator = 'N'
                db.session.add(benefit_rate)

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    @classmethod
    def update_all(cls, benefit_rates, plan_id):
        try:
            for benefit_rate in benefit_rates:
                db.session.add(benefit_rate)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    @classmethod
    def save_all_to_db(cls, benefit_rates, benefit_id):
        try:
            cls.expire_by_benefit(benefit_id)
            for benefit_rate in benefit_rates:
                db.session.add(benefit_rate)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
