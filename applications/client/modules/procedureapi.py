import datetime
import json_plus
import unittest
from gluon import current

class ProcedureApi():

    def __init__(self, procedure_name):
        self.procedure_name = procedure_name

    def write_value(self, dictionary):
        """ Writes key value pairs into the values table
        param dictionary: Takes dictionary of key/value pairs as input
        """
        db = current.db
        for key,val in dictionary.iteritems():
            # Update the key value for this module if it already exists
            db.module_values.update_or_insert((db.module_values.name == key) & (db.module_values.modulename == self.procedure_name),
                                              time_stamp=datetime.datetime.utcnow(),
                                              modulename=self.procedure_name,
                                              name=key,
                                              module_value==json_plus.Serializable().dumps(val))


    def write_output(self, name, data, tag):
        """ This write the values and the tag to the outputs table.
        param name : This is the name of the output
         param data : The value of the output : This is a dictionary of key value pairs
         Param tag: This is the ID of the sensor (or additional data to differentiate the outputs)"""
        db = current.db
        data = json_plus.Serializable().dumps(data)
        db.outputs.insert(modulename=self.procedure_name,
                          name=name,
                          output_value=data,
                          time_stamp=datetime.datetime.utcnow(),
                          tag=tag)

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


#class TestProcedureAPI(unittest.TestCase):

#    def test_output(self):
#       dict = {"temperature": 31, "humidity": 45}
#        api = ProcedureApi("TestModule23")
#        api.write_output("Thermostat Readings", dict, "None")
#        db = current.db
#        row = db(db.outputs.modulename == "TestModule23").select()
#       output_val = row[0].output_value
#        self.assertEqual(dict, json_plus.Serializable().loads(output_val))
