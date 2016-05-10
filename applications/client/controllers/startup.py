def start():
    """Here we need to load the scheduler with the correct schedules,
    avoiding any duplication . See the slugiot_synchronization module."""
    # REMOVE similar things from the scheduler.
    db(db.scheduler_task.task_name == 'synch').delete()
    slugiot_scheduler.queue_task(
        task_name='synch',
        function='do_synchronization',
        pvars={},
        repeats=0,
        period=60,
        retry_failed=0)
    current.db.commit();

    db(db.scheduler_task.task_name == 'proc_synch').delete()
    slugiot_scheduler.queue_task(
        task_name='synch',
        function='do_procedure_sync',
        pvars={},
        repeats=0,
        period=60,
        retry_failed=0)
    current.db.commit();
