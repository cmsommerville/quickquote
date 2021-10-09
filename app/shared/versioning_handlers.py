from .VersionedTable import VersionedTable
from sqlalchemy import func, inspect
from sqlalchemy.orm import make_transient, class_mapper
from sqlalchemy.orm.util import has_identity


def expire_old_records(session, flush_context, instances):
    # updates must come before adds
    updateHandler(session)
    newHandler(session)


def newHandler(session):
    for instance in session.new:
        if not isinstance(instance, VersionedTable):
            continue
        if not session.is_modified(instance):
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
            c.row_exp_dts: func.current_timestamp(),
            c.updated_dts: func.current_timestamp()
        })


def updateHandler(session):
    for instance in session.dirty:
        if not isinstance(instance, VersionedTable):
            continue
        if not session.is_modified(instance):
            continue
        if not has_identity(instance):
            continue

        make_transient(instance)

        ##############################################
        # determine the primary key
        class_map = class_mapper(instance.__class__)
        pk = class_map.primary_key[0].name

        setattr(instance, pk, None)
        instance.row_eff_dts = None
        instance.row_exp_dts = None
        instance.active_record_indicator = None

        session.add(instance)
