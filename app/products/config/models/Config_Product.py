from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES

CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']

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
        "Model_ConfigProductVariation", back_populates="product")
    benefits = db.relationship(
        "Model_ConfigBenefit", back_populates="product")
    provisions = db.relationship(
        "Model_ConfigProvision", back_populates="product")
    states = db.relationship(
        "Model_ConfigProductStateAvailability", back_populates="product")

