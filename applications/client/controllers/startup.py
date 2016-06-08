from gluon import current
import datetime
import procedureapi

db = current.db
ramdb = current.ramdb

def _startup():
    """Since this is the only place at which the task is scheduled, it is safe to
    simply delete and recreate tasks at each startup (the parameters don't change)"""

    if not (request.env.HTTP_HOST.startswith('localhost') |
                request.env.HTTP_HOST.startswith('127')):
        raise (HTTP(403))

    # We remove all the schedules...
    current.ramdb.scheduler_task.truncate()
    # ... and all the procedure states, so the procedures have to run their
    # init() methods and re-create their appropriate schedules.
    current.ramdb.procedure_state.truncate()
    current.ramdb.commit()

    proc_rows = db(db.procedures).select()
    for row in proc_rows:
        api = procedureapi.ProcedureApi(row.name)
        api.add_schedule()
        logger.info("Added schedule for procedure %r", row.name)


    start_time = datetime.datetime.now()

    current.slugiot_scheduler.queue_task(
        task_name='do_procedure_sync',
        function='do_procedure_sync',
        start_time=start_time,
        pvars={},
        repeats=100000000000000,
        period=20,
        timeout=15,
        retry_failed=0
    )
    current.ramdb.commit()


    current.slugiot_scheduler.queue_task(
        task_name='do_synchronization',
        function='do_synchronization',
        start_time=start_time,
        pvars={},
        repeats=100000000000000,
        period=20,
        timeout=15,
        retry_failed=0
    )
    current.ramdb.commit()


def clear_all_tasks():
    """Here we clear all tasks"""
    current.ramdb(ramdb.scheduler_task).delete()
    current.ramdb.commit()
