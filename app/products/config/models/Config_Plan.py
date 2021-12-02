from app.extensions import db
from app.shared import BaseModel, BaseModel

from .constants import TBL_NAMES
from .Config_States import REF_STATE, Model_RefStates

REF_PRODUCT = TBL_NAMES['REF_PRODUCT']
REF_STATE = TBL_NAMES['REF_STATE']
CONFIG_PLAN = TBL_NAMES['CONFIG_PLAN']
CONFIG_PLAN_STATE_AVAILABILITY = TBL_NAMES['CONFIG_PLAN_STATE_AVAILABILITY']


class Model_RefProduct(BaseModel):
    __tablename__ = REF_PRODUCT

    product_code = db.Column(db.String(30), primary_key=True)
    product_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Product Code: {self.product_code}>"

    @classmethod
    def find(cls, code):
        return cls.query.filter(cls.product_code == code).first()


class Model_ConfigPlan(BaseModel):
    __tablename__ = CONFIG_PLAN
    __table_args__ = {
        "info": {"nk": ["product_code"]}
    }

    plan_id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(
        db.String(30), db.ForeignKey(f"{REF_PRODUCT}.product_code"))
    plan_effective_date = db.Column(db.Date, nullable=False)
    plan_expiration_date = db.Column(db.Date, nullable=False)

    product = db.relationship("Model_RefProduct")
    plan_variations = db.relationship(
        "Model_ConfigPlanVariations", back_populates="plan")
    coverages = db.relationship(
        "Model_ConfigCoverage", back_populates="plan")
    provisions = db.relationship(
        "Model_ConfigProvision", back_populates="plan")

    def __repr__(self):
        return f"<Plan Id: {self.plan_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.plan_id == id).first()

    @classmethod
    def find_qry(cls, id):
        return cls.query.filter(cls.plan_id == id)


class Model_ConfigPlanStateAvailability(BaseModel):
    __tablename__ = CONFIG_PLAN_STATE_AVAILABILITY

    plan_state_availability_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey(
        f"{CONFIG_PLAN}.plan_id"))
    state_code = db.Column(
        db.String(2), db.ForeignKey(f"{REF_STATE}.state_code"))
    state_effective_date = db.Column(db.Date, nullable=False)
    state_expiration_date = db.Column(db.Date, nullable=False)
