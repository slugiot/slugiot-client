# Web2py Scheduler

def run_procedure(procedure_name, method):
    proc = __import__(procedure_name)
    methodToCall = getattr(proc, method)
    result = methodToCall()
    logger.info("--------result from procedure call: " + result + "------------")
    pass


from gluon.scheduler import Scheduler
current.slugiot_scheduler = Scheduler(db, dict(rerun_procedure=run_procedure))
