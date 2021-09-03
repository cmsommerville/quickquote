from app.models import db
import datetime


class ProvisionModel(db.Model):
    __tablename__ = "provisions"

    provision_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    provision_code = db.Column(db.String(20), nullable=False)
    provision_name = db.Column(db.String(100), nullable=False)
    provision_value = db.Column(db.String(255), nullable=False)
    provision_data_type = db.Column(db.String(20), nullable=False)
    row_add_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    plan = db.relationship("PlanModel", back_populates="provisions")

    def __repr__(self):
        return f"<Provision Id: {self.provision_id} -- Provision Name: `{self.provision_name}`>"

    def getValue(self):
        if self.provision_data_type == 'number':
            if '.' in self.provision_value:
                return float(self.provision_value)
            return int(self.provision_value)
        if self.provision_data_type == 'boolean':
            return self.provision_value.lower() == 'true'
        return self.provision_value

    def reset(self, data):
        self.plan_id = data.get("plan_id", self.plan_id)
        self.provision_code = data.get("provision_code", self.provision_code)
        self.provision_name = data.get("provision_name", self.provision_name)
        self.provision_value = data.get(
            "provision_value", self.provision_value)
        self.provision_data_type = data.get(
            "provision_data_type", self.provision_data_type)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.provision_id == id).first()

    @classmethod
    def find_plan_provisions(cls, plan_id):
        return cls.query.filter(cls.plan_id == plan_id).all()

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
        else:
            db.session.commit()

    @classmethod
    def save_all_to_db(cls, provisions):
        try:
            for provision in provisions:
                db.session.add(provision)
        except:
            db.session.rollback()
        else:
            db.session.commit()