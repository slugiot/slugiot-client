from gluon import current

def start_synchronization():
    """Here we need to load the scheduler with the correct schedules,
    avoiding any duplication . See the slugiot_synchronization module."""
    # REMOVE similar things from the scheduler.
    db(db.scheduler_task.task_name == 'synchronize').delete()
    current.slugiot_scheduler.queue_task(
        task_name='synchronize',
        function='synchronize',
        pvars={},
        repeats=0,
        period=10,
        retry_failed=0)
    current.db.commit()


def test():
    # REMOVE similar things from the scheduler.
    db(db.scheduler_task.task_name == 'test_scheduler').delete()
    current.slugiot_scheduler.queue_task(
        task_name='test_scheduler',
        function='test_scheduler',
        pvars={},
        repeats=1,
        retry_failed=0)
    current.db.commit()



def clear_all_tasks():
    """Here we clear all tasks"""
    current.db(db.scheduler_task).delete()
    current.db.commit()


