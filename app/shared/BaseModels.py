from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.inspection import inspect
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

    def __repr__(self): 
        """
        Print instance as <[Model Name]: [Row SK]>
        """
        return f'<{self.__class__.__name__}: {getattr(self, inspect(self.__class__).primary_key[0].name)}>'

    @classmethod
    def find_one(cls, id, *args, **kwargs):
        pk1 = inspect(cls).primary_key[0]
        return cls.query.filter(pk1 == id).first()

    @classmethod
    def find_all(cls, limit=10, offset=1, *args, **kwargs):
        pk1 = inspect(cls).primary_key[0]
        return cls.query.order_by(pk1).slice(offset, offset+limit).all()

    @classmethod
    def save_all_to_db(cls, data):
        try:
            db.session.add_all(data)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

