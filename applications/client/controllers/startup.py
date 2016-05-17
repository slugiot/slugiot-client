def start():
    """NB: procedureapi.add_schedule() could have been used to add sync schedules
    by passing a dummy procedure name, but this is the only place where scheduling
    of these functions occurs, and it seemed safer to create tasks directly.  Also,
    since this is the only place at which the task is scheduled, it is safe to
    simply delete and recreate tasks at each startup (the parameters don't change)"""

    from gluon import current
    import datetime

    start_time = datetime.datetime.now()

    db(db.scheduler_task.task_name == 'do_procedure_sync').delete()
    db(db.scheduler_task.task_name == 'do_synchronization').delete()

    slugiot_scheduler.queue_task(
        task_name='do_procedure_sync',
        function='proc_sync',
        start_time=start_time,
        pvars={},
        repeats=0,
        period=60,
        timeout=60,
        retry_failed=1,
        num_retries = 1
    )
    current.db.commit();


    slugiot_scheduler.queue_task(
        task_name='do_synchronization',
        function='synchronize',
        start_time=start_time,
        pvars={},
        repeats=0,
        period=60,
        timeout=60,
        retry_failed=1,
        num_retries=1
    )
    current.db.commit();
