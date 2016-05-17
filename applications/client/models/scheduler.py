# Web2py Scheduler

import json_plus
from procedureapi import ProcedureApi

# Note: remember to schedule a procedure to run whenever it is downloaded
# to the device.

def run_procedure(module_name, class_name, function_args):
    # Builds the API.
    api = ProcedureApi(module_name)
    def log_both(msg):
        logger.info(msg)
        api.log_info(msg)
    proc_name = str(module_name)
    proc = __import__(proc_name)
    logger.info(proc_name)
    logger.info(proc)
    log_both("Calling procedure %s with arguments %r" % (module_name, function_args))
    # Gets the previous run, if any.
    previous_run = db((db.procedure_state.procedure_id == module_name) &
                      (db.procedure_state.class_name == class_name)).select(
        orderby=~db.procedure_state.time_stamp).first()
    if previous_run is None:
        # This is the first time the procedure runs.
        # We instantiate the class.
        procedure = getattr(proc, class_name)()
        procedure.api = api
        # First-time initialization.
        procedure.init()
    else:
        # Not the first run.  We can rescue the previous state.
        procedure = json_plus.Serializable.from_json(previous_run.procedure_state)
        procedure.api = api
        # We run it.
        procedure.run(*function_args)

    log_both("Procedure %s run ended." % module_name)
    # And serialize the output for the next run.
    procedure_state_serialized = procedure.to_json()
    api.log_info("Procedure state: %s " % procedure_state_serialized)
    db.procedure_state.insert(procedure_id=module_name,
                              class_name=class_name,
                              procedure_state=procedure_state_serialized)
    db.commit()

def synchronize():
    import slugiot_synchronization
    logger.info("Start synch")
    slugiot_synchronization.synch_all(slugiot_setup, ['logs', 'outputs', 'values'])
    logger.info("Synch was successful")


def proc_sync(function):
    import json_plus
    result = function()
    logger.info("Returned from procedure sync function call")
    logger.info(result)


from gluon.scheduler import Scheduler
current.slugiot_scheduler = Scheduler(db, dict(rerun_procedure=run_procedure,
                                               do_synchronization=synchronize,
                                               do_procedure_sync=proc_sync
                                               ))



