from app.extensions import db
from app.shared import BaseModel

from .__constants__ import TBL_NAMES

CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_RATE_GROUP = TBL_NAMES['CONFIG_RATE_GROUP']
REF_RATE_GROUP = TBL_NAMES['REF_RATE_GROUP']
REF_RATE_TYPE = TBL_NAMES['REF_RATE_TYPE']

class Model_ConfigRateGroup(BaseModel):
    __tablename__ = CONFIG_RATE_GROUP
    __table_args__ = (
        db.UniqueConstraint('rate_group_code'),
    )

    rate_group_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.product_id"), nullable=False)
    rate_group_code = db.Column(db.ForeignKey(f"{REF_RATE_GROUP}.rate_group_code"))
    rate_type_code = db.Column(db.ForeignKey(f"{REF_RATE_TYPE}.rate_type_code"), nullable=False)

    rate_group = db.relationship("Model_RefRateGroup")
    rate_type = db.relationship("Model_RefRateType")
    product = db.relationship("Model_ConfigProduct")

    @classmethod
    def find_by_product(cls, id):
        return cls.query.filter(cls.product_id == id).all()


MY_TESTER = 'WOOT WOOT!'