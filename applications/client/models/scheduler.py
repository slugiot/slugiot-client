# Web2py Scheduler

def run_procedure(procedure, function, function_args):
    proc = __import__(procedure)
    method_to_call = getattr(proc, function)

    import json_plus
    result = method_to_call(*function_args)
    logger.info("Returned from function call")
    logger.info(result)


def synchronize(function):
    import json_plus
    result = function()
    logger.info("Returned from synchronization function call")
    logger.info(result)


def proc_sync(function):
    import json_plus
    result = function()
    logger.info("Returned from proc_sync function call")
    logger.info(result)


from gluon.scheduler import Scheduler
current.slugiot_scheduler = Scheduler(db, dict(rerun_procedure=run_procedure,
                                               do_synchronization=synchronize,
                                               do_procedure_sync=proc_sync)
                                      )

