from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']
REF_PROVISION = TBL_NAMES['REF_PROVISION']

class Model_ConfigProvision(BaseModel):
    __tablename__ = CONFIG_PROVISION
    __table_args__ = (
        db.UniqueConstraint('product_id', 'provision_code'),
        db.CheckConstraint('provision_effective_date <= provision_expiration_date')
    )

    provision_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.product_id"), nullable=False)
    provision_code = db.Column(db.ForeignKey(f"{REF_PROVISION}.provision_code"), nullable=False)
    provision_effective_date = db.Column(db.Date(), nullable=False)
    provision_expiration_date = db.Column(db.Date(), nullable=False)

    product = db.relationship(
        "Model_ConfigProduct", back_populates="provisions")
    provision = db.relationship("Model_RefProvision")
    states = db.relationship(
        "Model_ConfigProvisionStateAvailability", back_populates="provision")
    factors = db.relationship("Model_ConfigFactor")

    @classmethod
    def find_by_product(cls, id):
        return cls.query.filter(cls.product_id == id).all()