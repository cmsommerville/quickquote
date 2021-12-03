from app.extensions import db
from app.shared import BaseModel, BaseModel

from .constants import TBL_NAMES
from .Config_States import REF_STATE, Model_RefStates

REF_PRODUCT = TBL_NAMES['REF_PRODUCT']
REF_STATE = TBL_NAMES['REF_STATE']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PRODUCT_STATE_AVAILABILITY = TBL_NAMES['CONFIG_PRODUCT_STATE_AVAILABILITY']



class Model_ConfigProduct(BaseModel):
    __tablename__ = CONFIG_PRODUCT
    __table_args__ = (
        db.UniqueConstraint('product_code'),
    )

    product_id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(30), nullable=False)
    product_label = db.Column(db.String(100), nullable=False)
    product_effective_date = db.Column(db.Date, nullable=False)
    product_expiration_date = db.Column(db.Date, nullable=False)

    product_variations = db.relationship(
        "Model_ConfigProductVariations", back_populates="product")
    coverages = db.relationship(
        "Model_ConfigCoverage", back_populates="product")
    provisions = db.relationship(
        "Model_ConfigProvision", back_populates="product")

    def __repr__(self):
        return f"<Product ID: {self.product_id} - {self.product_code}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.product_id == id).first()


class Model_ConfigProductStateAvailability(BaseModel):
    __tablename__ = CONFIG_PRODUCT_STATE_AVAILABILITY
    __table_args__ = (
        db.UniqueConstraint('product_id', 'state_id', 'state_effective_date'),
        db.CheckConstraint('state_effective_date <= state_expiration_date')
    )

    product_state_availability_id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.product_code"), nullable=False)
    state_id = db.Column(db.ForeignKey(f"{REF_STATE}.state_id"), nullable=False)
    state_effective_date = db.Column(db.Date, nullable=False)
    state_expiration_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Product State Availability ID: {self.product_state_availability_id} - {self.state_effective_date}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.product_state_availability_id == id).first()
