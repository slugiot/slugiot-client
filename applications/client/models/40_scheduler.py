# Web2py Scheduler
# Here we define what functions we may want to schedule, and then create the scheduler
# DO NOT enqueue tasks here!  This is run on every page request, so we want to have
# the enqueuing of things happen somewhere else.

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
    slugiot_synchronization.synch_all_c2s(slugiot_setup)
    slugiot_synchronization.synchronize_settings(slugiot_setup)


def test_scheduler():
    print 'the scheduler is working'


from gluon.scheduler import Scheduler
current.slugiot_scheduler = Scheduler(db, dict(rerun_procedure=run_procedure,
                                               synchronize=scheduled_synchronize,
                                               test_scheduler=test_scheduler))

# For running the server with the scheduler:
# --with-scheduler --scheduler=client




