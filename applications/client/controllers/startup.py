from gluon import current
import datetime

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


    start_time = datetime.datetime.now()

    # TODO - change database to one specific to scheuler (as per recommendation in web2py docs)
    db(db.scheduler_task.task_name == 'do_procedure_sync').delete()
    db(db.scheduler_task.task_name == 'do_synchronization').delete()

    current.slugiot_scheduler.queue_task(
        task_name='do_procedure_sync',
        function='do_procedure_sync',
        start_time=start_time,
        pvars={},
        repeats=0,
        period=20,
        timeout=10,
        retry_failed=0
    )
    current.db.commit()


    current.slugiot_scheduler.queue_task(
        task_name='do_synchronization',
        function='do_synchronization',
        start_time=start_time,
        pvars={},
        repeats=0,
        period=20,
        timeout=10,
        retry_failed=0
    )
    current.db.commit()



def clear_all_tasks():
    """Here we clear all tasks"""
    current.db(db.scheduler_task).delete()
    current.db.commit()
