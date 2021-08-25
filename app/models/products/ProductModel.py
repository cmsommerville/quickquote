from app.models import db


class ProductModel(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_code = db.Column(db.String(10), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)

    @classmethod
    def find_by_id(cls, id):
        return db.session.query(cls).filter(cls.product_id == id).first()

    @classmethod
    def find_all(cls, num_rows=1000):
        return db.session.query(cls).limit(num_rows).all()

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
        else:
            db.session.commit()
