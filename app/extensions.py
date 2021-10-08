from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow
from sqlalchemy.orm.util import has_identity
from sqlalchemy import inspect
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm import Mapper

sess = Session()
db = SQLAlchemy()
mongo = PyMongo()
ma = Marshmallow()


def expire_old_records(sesh, flush_context, instances):
    # updates must come before adds
    updateHandler(sesh)
    newHandler(sesh)


def newHandler(sesh):
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


def updateHandler(sesh):
    for instance in sesh.dirty:
        if not isinstance(instance, db.Model):
            continue
        if not sesh.is_modified(instance):
            continue
        if not has_identity(instance):
            continue

        db.make_transient(instance)

        ##############################################
        # determine the primary key
        class_map = class_mapper(instance.__class__)
        pk = class_map.primary_key[0].name

        setattr(instance, pk, None)
        instance.row_eff_dts = None
        instance.row_exp_dts = None
        instance.active_record_indicator = None

        sesh.add(instance)
