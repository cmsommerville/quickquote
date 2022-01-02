from app.extensions import db
from app.shared import BaseModel
from ...__constants__ import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_BENEFIT_PRODUCT_VARIATION_APPLICABILITY = TBL_NAMES['CONFIG_BENEFIT_PRODUCT_VARIATION_APPLICABILITY']
CONFIG_PRODUCT_VARIATIONS = TBL_NAMES['CONFIG_PRODUCT_VARIATIONS']


class Model_ConfigBenefitProductVariation(BaseModel):
    __tablename__ = CONFIG_BENEFIT_PRODUCT_VARIATION_APPLICABILITY
    __table_args__ = (
        db.UniqueConstraint('benefit_id', 'product_variation_id'),
    )

    benefit_product_variation_id = db.Column(db.Integer, primary_key=True)
    benefit_id = db.Column(db.ForeignKey(f"{CONFIG_BENEFIT}.benefit_id"), nullable=False)
    product_variation_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT_VARIATIONS}.product_variation_id"), nullable=False)

    benefit = db.relationship(
        "Model_ConfigBenefit", back_populates="product_variations")
    product_variation = db.relationship(
        "Model_ConfigProductVariation", back_populates="benefits")

    @classmethod
    def find_product_variations(cls, id):
        return cls.query.filter(cls.benefit_id == id).all()

    @classmethod
    def find_benefits(cls, id):
        return cls.query.filter(cls.product_variation_id == id).all()
