# Web2py Scheduler
# Here we define what functions we may want to schedule, and then create the scheduler
# DO NOT enqueue tasks here!  This is run on every page request, so we want to have
# the enqueuing of things happen somewhere else.
import json_plus
from procedureapi import ProcedureApi

def run_procedure(module_name, class_name, function_args):
    # Builds the API.
    api = ProcedureApi(module_name)
    def log_both(msg):
        api.log_info(msg)

    proc_name = "procedures." + module_name
    proc = __import__(proc_name, fromlist=[''])

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


def scheduled_synchronize():
    import slugiot_synchronization
    slugiot_synchronization.synch_all_c2s(slugiot_setup)
    slugiot_synchronization.synchronize_settings(slugiot_setup)


def proc_sync(function):
    import json_plus
    result = function()


from gluon.scheduler import Scheduler
current.slugiot_scheduler = Scheduler(db, dict(run_procedure=run_procedure,
                                               do_synchronization=scheduled_synchronize,
                                               do_procedure_sync=proc_sync
                                               ))

# For running the server with the scheduler:
# --with-scheduler --scheduler=client




