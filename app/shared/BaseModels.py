from app.extensions import db
from .VersionedTable import VersionedTable


class BaseModel(db.Model):
    __abstract__ = True

    created_by = db.Column(db.String(50))
    created_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_dts = db.Column(db.DateTime, default=db.func.current_timestamp())

    @classmethod
    def save_all_to_db(cls, data):
        try:
            db.session.add_all(data)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    def save_to_db(self):
        try:
            db.session.add(self)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()


class BaseVersionedModel(BaseModel, VersionedTable):
    __abstract__ = True

    row_eff_dts = db.Column(db.DateTime, default=db.func.current_timestamp())
    row_exp_dts = db.Column(db.DateTime, default='9999-12-31 00:00:00.000')
    active_record_indicator = db.Column(db.String(1), default='Y')
