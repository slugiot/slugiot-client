# Web2py Scheduler

def run_procedure(args):
    # Call the procedure again
    #procedure_name = args[0]
    # Need to get the latest version of the procedure
    # If the procedure is present in the predetermined location, run it
    # Otherwise we may need to get the procedure from the DB (?)
    import time
    print(time.ctime())
    print("blah")
    logger.error("time: " + time.ctime())
    pass


from gluon.scheduler import Scheduler
current.scheduler1 = Scheduler(db, dict(recurrun=run_procedure))
