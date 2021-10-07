from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow

sess = Session()
db = SQLAlchemy()
mongo = PyMongo()
ma = Marshmallow()


def expire_old_records(sesh, flush_context, instances):
    for instance in sesh.new:
        if not isinstance(instance, db.Model):
            continue
        if not sesh.is_modified(instance):
            continue
        if not getattr(instance, 'plan_id', None):
            continue

        plan_id = instance.plan_id
        c = instance.__class__
        c.query.filter(
            c.active_record_indicator == 'Y',
            c.plan_id == plan_id
        ).update({
            c.active_record_indicator: 'N',
            c.row_exp_dts: db.func.current_timestamp(),
            c.updated_dts: db.func.current_timestamp()
        })
