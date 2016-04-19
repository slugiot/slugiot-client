<<<<<<< HEAD
=======
import datetime
from gluon import current

>>>>>>> 344aa639277a13c362b3dd605db340846c4a351c
class ProcedureApi():

    def __init__(self, procedure_name):
        self.procedure_name = procedure_name

    def write_value(**dictionary):		#This function will be called by the (?)harness team(?) and they will be passing a dictionary as the argument
        for key in dictionary:
	        ModuleName = dictionary['module_name'];
		ModuleValues = dictionary['module_value'];
		VariableName = dictionary['variable_name'];
	TimeStamp = datetime.datetime.utcnow();	
	current.db.module_values.insert(modulename=ModuleName);
	current.db.module_values.insert(name=VariableName);
	current.db.module_values.insert(module_value=ModuleValues);
	current.db.module_values.insert(time_stamp = TimeStamp);

    def write_output(self, name, data, tag):
        pass

    def write_log(self, log_text, log_level=0):
<<<<<<< HEAD
        pass

    # todo : schedule tasks for procedure
    def add_schedule(self):
        pass
=======
        current.db.logs.insert(time_stamp=datetime.datetime.utcnow())

#                               modulename=self.procedure_name,
#                               log_level=log_level,
#                               log_message=log_text)

    # todo : schedule tasks for procedure
    def add_schedule(self):
        pass

>>>>>>> 344aa639277a13c362b3dd605db340846c4a351c
