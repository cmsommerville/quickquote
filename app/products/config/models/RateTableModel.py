from app.extensions import db
import datetime


class RateTableModel(db.Model):
    __tablename__ = "rate_table"

    rate_table_id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(20), nullable=False)
    product_variation_code = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    family_code = db.Column(db.String(3), nullable=False)
    smoker_status = db.Column(db.String(1), nullable=False)
    benefit_code = db.Column(db.String(20), nullable=False)
    annual_rate_per_unit = db.Column(db.Numeric(12, 5))
    unit_value = db.Column(db.Numeric(12, 5))

    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    __table_args__ = (db.UniqueConstraint(
        'product_code', 'product_variation_code', 'benefit_code',
        'age', 'family_code', 'smoker_status',
        name='rate_table__ukey'), )

    def __repr__(self):
        return f"<Rate Table Id: {self.rate_table_id} - Product Code: {self.product_code}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.rate_table_id == id).first()

    @classmethod
    def find_benefit_rateset(cls, product_code, product_variation_code, benefit):
        return cls.query.filter(
            cls.product_code == product_code,
            cls.product_variation_code == product_variation_code,
            cls.benefit == benefit).all()

    @classmethod
    def save_all_to_db(cls, rates):
        try:
            for rate in rates:
                db.session.add(rate)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()
