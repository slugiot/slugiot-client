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


from gluon.scheduler import Scheduler
current.slugiot_scheduler = Scheduler(db, dict(rerun_procedure=run_procedure,
                                               do_synchronization=scheduled_synchronize))
# current.slugiot_scheduler.queue_task('do_synchronization', period=10, repeats=0)
# --with-scheduler --scheduler=client




