from app.extensions import db
from app.shared import BaseModel

from .constants import TBL_NAMES

REF_RATE_GROUP = TBL_NAMES['REF_RATE_GROUP']
REF_RATE_TYPE = TBL_NAMES['REF_RATE_TYPE']
CONFIG_PRODUCT= TBL_NAMES['CONFIG_PRODUCT']
CONFIG_RATE_GROUP = TBL_NAMES['CONFIG_RATE_GROUP']


class Model_RefRateGroup(BaseModel):
    __tablename__ = REF_RATE_GROUP

    rate_group_code = db.Column(db.String(30), primary_key=True)
    rate_group_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Rate Group Code: {self.rate_group_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.rate_group_code == code).first()


class Model_RefRateType(BaseModel):
    __tablename__ = REF_RATE_TYPE

    rate_type_code = db.Column(db.String(30), primary_key=True)
    rate_type_label = db.Column(db.String(100))

    def __repr__(self):
        return f"<Rate Type Code: {self.rate_type_code}>"

    @classmethod
    def find(cls, code: str):
        return cls.query.filter(cls.rate_type_code == code).first()


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

    def __repr__(self):
        return f"<Rate Group Id: {self.rate_group_id}>"

    @classmethod
    def find(cls, id):
        return cls.query.filter(cls.rate_group_id == id).first()

    @classmethod
    def find_by_product(cls, id):
        return cls.query.filter(cls.product_id == id).all()