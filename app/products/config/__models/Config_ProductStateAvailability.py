from app.extensions import db, ma
from app.shared import BaseModel, BaseSchema, CRUD_ResourceFactory

from .constants import TBL_NAMES
from .Config_Product import Schema_ConfigProduct
from .Ref_States import Schema_RefStates

CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PRODUCT_STATE_AVAILABILITY = TBL_NAMES['CONFIG_PRODUCT_STATE_AVAILABILITY']
REF_STATE = TBL_NAMES['REF_STATE']

class Model_ConfigProductStateAvailability(BaseModel):
    __tablename__ = CONFIG_PRODUCT_STATE_AVAILABILITY
    __table_args__ = (
        db.UniqueConstraint('product_id', 'state_id', 'state_effective_date'),
        db.CheckConstraint('state_effective_date <= state_expiration_date')
    )

    product_state_id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.product_id"), nullable=False)
    state_id = db.Column(db.ForeignKey(f"{REF_STATE}.state_id"), nullable=False)
    state_effective_date = db.Column(db.Date, nullable=False)
    state_expiration_date = db.Column(db.Date, nullable=False)

    product = db.relationship("Model_ConfigProduct", back_populates="states")
    state = db.relationship("Model_RefStates")

    @classmethod
    def find_by_product(cls, id):
        return cls.query.filter(cls.product_id == id).all()

