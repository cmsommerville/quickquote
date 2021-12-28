from app.extensions import db
from app.shared import BaseModel

from ...__constants__ import TBL_NAMES, COVERAGE_SECTION_DEFAULT

CONFIG_COVERAGE = TBL_NAMES['CONFIG_COVERAGE']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']

class Model_ConfigCoverage(BaseModel):
    __tablename__ = CONFIG_COVERAGE
    __table_args__ = (
        db.UniqueConstraint('coverage_code'),
    )

    coverage_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.product_id"), nullable=False)
    coverage_code = db.Column(db.String(30), nullable=False)
    coverage_label = db.Column(db.String(100), nullable=False)
    section_code = db.Column(db.String(30), default=COVERAGE_SECTION_DEFAULT)

    benefits = db.relationship("Model_ConfigBenefit", back_populates="coverage")

    @classmethod
    def find_by_product(cls, id: int):
        return cls.query.filter(cls.product_id == id).all()
