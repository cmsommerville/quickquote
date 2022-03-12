from app.extensions import db
from app.shared import BaseModel
import datetime


class RateTableModel(BaseModel):
    __tablename__ = "rate_table2"

    rate_table_id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(20), nullable=False)
    product_variation_code = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    family_code = db.Column(db.String(3), nullable=False)
    smoker_status = db.Column(db.String(1), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    benefit_code = db.Column(db.String(20), nullable=False)
    annual_rate_per_unit = db.Column(db.Numeric(12, 5))
    unit_value = db.Column(db.Numeric(12, 5))

    __table_args__ = (db.UniqueConstraint(
        'product_code', 'product_variation_code', 'benefit_code',
        'age', 'family_code', 'smoker_status', 'gender',
        name='rate_table__ukey'), )

    def __repr__(self):
        return f"<Rate Table Id: {self.rate_table_id} - Product Code: {self.product_code}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.rate_table_id == id).first()

    @classmethod
    def find_benefit_rateset(cls, product_code, product_variation_code, benefit_code):
        return cls.query.filter(
            cls.product_code == product_code,
            cls.product_variation_code == product_variation_code,
            cls.benefit_code == benefit_code).all()

    @classmethod
    def find_many_benefit_ratesets(cls, product_code, product_variation_code, benefit_codes):
        return cls.query.filter(
            cls.product_code == product_code,
            cls.product_variation_code == product_variation_code,
            cls.benefit_code.in_(benefit_codes)).all()
