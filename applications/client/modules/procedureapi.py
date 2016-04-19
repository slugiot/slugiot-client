import datetime
from gluon import current

class ProcedureApi():

    def __init__(self, procedure_name):
        self.procedure_name = procedure_name

    def write_value(**dictionary):
    	db = current.db
    # This function will be called by the (?)harness team(?) and they will be passing a dictionary as the argument
        for key in dictionary:
            ModuleValues = dictionary['module_value']
            VariableName = dictionary['variable_name']
        TimeStamp = datetime.datetime.utcnow()
	ModuleName = self.procedure_name
        db.module_values.insert(modulename=ModuleName,
				name=VariableName,
        			module_value=ModuleValues,
        			time_stamp=TimeStamp)


    def write_output(self, name, data, tag):
        pass

    def write_log(self, log_text, log_level=0):
        """Writes a log message to the logs table
        param log_text : message to be logged
        param log_level : 0 for error, 1 for warning, 2 for info, 3 for debug """
        db = current.db
        db.logs.insert(time_stamp=datetime.datetime.utcnow(),
                       modulename=self.procedure_name,
                       log_level=log_level,
                       log_message=log_text)

    # todo : schedule tasks for procedure
    def add_schedule(self):
        pass

