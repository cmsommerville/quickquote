from app.extensions import db
from sqlalchemy import Table

def alter_versioned_table(table_instance: Table) -> None: 

    ROW_EFF_DTS = 'row_eff_dts'
    ROW_EXP_DTS = 'row_exp_dts'

    if table_instance.schema:
        tbl = table_instance.schema + "." + table_instance.name
    else:
        tbl = "dbo." + table_instance.name

    sql = f"""
    ALTER TABLE {tbl}
    ADD 
        {ROW_EFF_DTS} DATETIME2 GENERATED ALWAYS AS ROW START HIDDEN NOT NULL DEFAULT GETUTCDATE(),
        {ROW_EXP_DTS} DATETIME2 GENERATED ALWAYS AS ROW END HIDDEN  NOT NULL DEFAULT CONVERT(DATETIME2, '9999-12-31 23:59:59.9999999'),
    PERIOD FOR SYSTEM_TIME ({ROW_EFF_DTS}, {ROW_EXP_DTS})

    ALTER TABLE {tbl}
    SET (SYSTEM_VERSIONING = ON (HISTORY_TABLE={tbl}_history))
    """

    db.session.execute(sql)
    db.session.commit()

def toggle_system_versioning(table_instance: Table) -> None:

    if table_instance.schema:
        tbl = table_instance.schema + "." + table_instance.name
    else:
        tbl = "dbo." + table_instance.name

    sql = f"""
    ALTER TABLE {tbl} SET ( SYSTEM_VERSIONING = OFF  )
    GO
    """

    db.session.execute(sql)
    db.session.commit()



def drop_history_table(table_instance: Table) -> None:

    if table_instance.schema:
        tbl = table_instance.schema + "." + table_instance.name
    else:
        tbl = "dbo." + table_instance.name

    sql = f"""
    ALTER TABLE {tbl} SET ( SYSTEM_VERSIONING = OFF )
    """
    try: 
        db.session.execute(sql)
        db.session.commit()
    except: 
        db.session.rollback()

    sql = f"""
    DROP TABLE {tbl}_history
    """
    try: 
        db.session.execute(sql)
        db.session.commit()
    except: 
        db.session.rollback()