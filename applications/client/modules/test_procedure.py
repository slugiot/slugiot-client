import procedureapi
import logging

logger = logging.getLogger()
api = procedureapi.ProcedureApi("test_procedure")

def run():
    # Add schedules
    api.add_schedule("method1", repeats=5, period=10)
    api.add_schedule("method2", repeats=5, period=10)

def method1():
    logger.error("----------In method1!!-----------")
    return "Just executed method1"

def method2():
    logger.error("-----------In method2!!------------")
    return "Just executed method2"

#from gluon import current
#from gluon import DAL
#os.copy('mysafecopy.sql', 'myfile.sql')
#tdb = DAL('sqlite:myfile.sql')
#current.db = tdb