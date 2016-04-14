import datetime
from gluon import current

class ProcedureApi():

    def __init__(self, procedure_name):
        self.procedure_name = procedure_name

    def write_value(self, name, data):
        pass

    def write_output(self, name, data, tag):
        pass

    def write_log(self, log_text, log_level=0):
        current.db.logs.insert(time_stamp=datetime.datetime.utcnow())

#                               modulename=self.procedure_name,
#                               log_level=log_level,
#                               log_message=log_text)

    # todo : schedule tasks for procedure
    def add_schedule(self):
        pass

