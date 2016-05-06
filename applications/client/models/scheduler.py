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
    logger.info("Start synch")
    slugiot_synchronization.synch_all(slugiot_setup, ['logs', 'outputs', 'values'])
    logger.info("Synch was successful")


from gluon.scheduler import Scheduler
current.slugiot_scheduler = Scheduler(db, dict(rerun_procedure=run_procedure,
                                               do_synchronization=scheduled_synchronize))



