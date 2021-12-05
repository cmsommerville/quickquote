from sqlalchemy.ext.declarative import declared_attr
from app.extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    @declared_attr
    def created_by(cls):
        return db.Column(db.String(50))

    @declared_attr
    def created_dts(cls):
        return db.Column(db.DateTime, default=db.func.current_timestamp())

    @declared_attr
    def updated_dts(cls):
        return db.Column(db.DateTime, default=db.func.current_timestamp())

    @classmethod
    def save_all_to_db(cls, data):
        try:
            db.session.add_all(data)
        except Exception:
            db.session.rollback()
            raise

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def save_to_db(self):
        try:
            db.session.add(self)
        except Exception:
            db.session.rollback()
            raise

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise


    def delete(self):
        try:
            db.session.delete(self)
        except Exception:
            db.session.rollback()
            raise

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

