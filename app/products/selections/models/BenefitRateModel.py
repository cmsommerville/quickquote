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

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    plan = db.relationship("PlanModel")
    benefit = db.relationship("BenefitModel", back_populates="benefit_rates")
    factors = db.relationship("FactorModel", back_populates="benefit_rate")

    def __repr__(self):
        return f"<Benefit Rate Id: {self.benefit_rate_id}>"

    def reset(self, **kwargs):
        self.benefit_id = kwargs.get('benefit_id', self.benefit_id)
        self.plan_id = kwargs.get('plan_id', self.plan_id)
        self.age = kwargs.get('age', self.age)
        self.family_code = kwargs.get('family_code', self.family_code)
        self.smoker_status = kwargs.get('smoker_status', self.smoker_status)
        self.benefit_rate_uuid = kwargs.get(
            'benefit_rate_uuid', self.benefit_rate_uuid)
        self.benefit_rate_base_premium = kwargs.get(
            'benefit_rate_base_premium', self.benefit_rate_base_premium)
        self.benefit_rate_factor = None
        self.benefit_rate_benefit_factor = None
        self.benefit_rate_final_premium = None
        self.updated_dts = db.func.now()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.benefit_rate_id == id).first()

    @classmethod
    def find_benefit_rates_by_plan(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id).options(db.joinedload(cls.benefit)).all()

    @classmethod
    def find_benefit_rates_by_benefit(cls, benefit_id):
        return cls.query.filter(cls.benefit_id == benefit_id).options(db.joinedload(cls.benefit)).all()

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    @classmethod
    def save_all_to_db(cls, benefit_rates, benefit_id):
        try:
            for benefit_rate in benefit_rates:
                db.session.add(benefit_rate)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
