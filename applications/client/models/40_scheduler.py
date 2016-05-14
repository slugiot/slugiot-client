# Web2py Scheduler

def run_procedure(procedure, function, function_args):
    proc = __import__(procedure)
    method_to_call = getattr(proc, function)

    # import json_plus
    logger.info("Calling %s.%s %r" % (procedure, function, function_args))
    result = method_to_call(*function_args)
    logger.info("Returned from function call")
    logger.info("%r" % result)


def scheduled_synchronize():
    import slugiot_synchronization
    slugiot_synchronization.synch_all(slugiot_setup, ['logs', 'outputs'])


########
def test_scheduler():
    print 'Test'
    return 'done!'
#########
from gluon.scheduler import Scheduler
current.slugiot_scheduler = Scheduler(db, dict(rerun_procedure=run_procedure,
                                               do_synchronization=scheduled_synchronize,
                                               test_scheduler=test_scheduler))
current.slugiot_scheduler.queue_task(function='test_scheduler', period=5, repeats=1, timeout=60,
                                    immediate=True,)
current.db.commit()
# --with-scheduler --scheduler=client




