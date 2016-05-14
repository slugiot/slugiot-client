# Web2py Scheduler

import json_plus
from procedureapi import ProcedureApi

# Note: remember to schedule a procedure to run whenever it is downloaded
# to the device.

def run_procedure(procedure_id, class_name, function_args):
    # Builds the API.
    api = ProcedureApi(procedure_id)
    def log_both(msg):
        logger.info(msg)
        api.log_info(msg)
    proc_name = str(procedure_id) + '.py'
    proc = __import__(proc_name)
    log_both("Calling procedure_id %s with arguments %r" % (procedure_id, function_args))
    # Gets the previous run, if any.
    previous_run = db((db.procedure_state.procedure_id == procedure_id) &
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
        procedure.run()

    log_both("Procedure %s run ended." % procedure_id)
    # And serialize the output for the next run.
    db.procedure_state.insert(procedure_id=procedure_id,
                              class_name=class_name,
                              procedure_state=procedure.to_json())
    db.commit()

def synchronize():
    import slugiot_synchronization
    logger.info("Start synch")
    slugiot_synchronization.synch_all(slugiot_setup, ['logs', 'outputs', 'values'])
    logger.info("Synch was successful")


from gluon.scheduler import Scheduler
current.slugiot_scheduler = Scheduler(db, dict(run_procedure=run_procedure,
                                               do_synchronization=synchronize))



