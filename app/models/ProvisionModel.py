from app.models import db
import datetime


class ProvisionModel(db.Model):
    __tablename__ = "provisions"

    provision_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    provision_code = db.Column(db.String(20), nullable=False)
    provision_value = db.Column(db.String(255), nullable=False)
    provision_data_type = db.Column(db.String(20), nullable=False)

    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(
        db.DateTime, default=datetime.datetime(9999, 12, 31, 0, 0, 0))
    active_record_indicator = db.Column(db.String(1), default='Y')

    plan = db.relationship("PlanModel", back_populates="provisions")

    def __repr__(self):
        return f"<Provision Id: {self.provision_id} -- Provision Code: `{self.provision_code}`>"

    def getValue(self):
        if self.provision_data_type == 'number':
            if '.' in self.provision_value:
                return float(self.provision_value)
            return int(self.provision_value)
        if self.provision_data_type == 'boolean':
            return self.provision_value.lower() == 'true'
        return self.provision_value

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.provision_id == id).first()

    @classmethod
    def find_plan_provisions(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id, cls.active_record_indicator == 'Y').all()

    @classmethod
    def expire_provisions(cls, plan_id):
        provisions = cls.find_plan_provisions(plan_id)
        if provisions:
            for provision in provisions:
                provision.row_exp_dts = db.func.current_timestamp()
                provision.active_record_indicator = 'N'
                db.session.add(provision)

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    @classmethod
    def save_all_to_db(cls, provisions, plan_id):
        try:
            cls.expire_provisions(plan_id)
            for provision in provisions:
                db.session.add(provision)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
