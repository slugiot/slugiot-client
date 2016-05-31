from gluon import current
import datetime
import procedureapi

db = current.db
ramdb = current.ramdb

def _startup():
    """NB: procedureapi.add_schedule() could have been used to add sync schedules
    by passing a dummy procedure name, but this is the only place where scheduling
    of these functions occurs, and it seemed safer to create tasks directly.  Also,
    since this is the only place at which the task is scheduled, it is safe to
    simply delete and recreate tasks at each startup (the parameters don't change)"""

    # TODO - test this code to a check against external calls.  Also check on the underscore
    if not (request.env.HTTP_HOST.startswith('localhost') |
                request.env.HTTP_HOST.startswith('127')):
        raise (HTTP(403))

    current.ramdb.scheduler_task._truncate()
    current.ramdb.commit()

    proc_rows = db(db.procedures).select()
    for row in proc_rows:
        api = procedureapi.ProcedureApi(row.name)
        api.add_schedule()


    start_time = datetime.datetime.now()


    current.slugiot_scheduler.queue_task(
        task_name='do_procedure_sync',
        function='do_procedure_sync',
        start_time=start_time,
        pvars={},
        repeats=0,  # If repeats=0 (unlimited), it would constantly fail.
        period=30,
        timeout=60,
        retry_failed=1
    )
    current.ramdb.commit();


    current.slugiot_scheduler.queue_task(
        task_name='do_synchronization',
        function='do_synchronization',
        start_time=start_time,
        pvars={},
        repeats=1,  # If repeats=0 (unlimited), it would constantly fail.
        period=600,
        timeout=60,
        retry_failed=5
    )
    current.ramdb.commit();



def clear_all_tasks():
    """Here we clear all tasks"""
    current.ramdb(ramdb.scheduler_task).delete()
    current.ramdb.commit()
