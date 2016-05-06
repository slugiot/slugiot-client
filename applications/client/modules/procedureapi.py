import datetime
import json_plus
from gluon import current
import slugiot_setup

class ProcedureApi():

    class LogLevel:
        """The log levels used for logging into the logs table"""
        ERROR = 0
        WARNING = 1
        INFO = 2
        DEBUG = 3

    def __init__(self, procedure_name):
        # Luca says: this needs to work by procedure_id to make things easy.
        # Let us know if this creates too much trouble.  We cannot refer
        # to procedures sometimes by id and sometimes by name.
        self.procedure_name = procedure_name

    def write_value(self, dictionary):
        """ Writes key value pairs into the values table
        param dictionary: Takes dictionary of key/value pairs as input
        """
        db = current.db
        for key,val in dictionary.iteritems():
            # Update the key value for this module if it already exists
            db.module_values.update_or_insert((db.module_values.name == key) & (db.module_values.modulename == self.procedure_name),
                                              time_stamp=datetime.datetime.utcnow(), # Luca: might not be necessary.
                                              modulename=self.procedure_name,
                                              name=key,
                                              module_value=json_plus.Serializable.dumps(val))
        db.commit()


    def read_value(self, key):
        """ Returns the value from the module_values table for a given key
        The lookup is done using the key and the procedure name
        param key : The key whose value needs to be returned"""
        db = current.db
        row = db((db.module_values.name == key) & (db.module_values.modulename == self.procedure_name)).select().first()
        return None if row is None else json_plus.Serializable.loads(row.module_value)


    def write_output(self, name, data, tag=None, timestamp=None):
        """ This write the value and the tag to the outputs table.
        param name : Name of the output
        param data : The value of the output
        Param tag: This is the ID of the sensor (or additional data to differentiate the outputs)"""
        db = current.db
        timestamp = timestamp or datetime.datetime.utcnow()
        db.outputs.insert(modulename=self.procedure_name,
                          name=name,
                          output_value=json_plus.Serializable.dumps(data),
                          time_stamp=datetime.datetime.utcnow(), # Luca: this might not be necessary. Same in the following.
                          tag=tag)
        db.commit()

    def write_outputs(self, data, tag=None):
        """ This write the values and the tag to the outputs table.
        param data : dict of key/value pairs to be written to the table. All pairs will have the same timestamp
        Param tag: This is the ID of the sensor (or additional data to differentiate the outputs)"""

        db = current.db
        time_now = datetime.datetime.utcnow()
        # Luca: check, rewritten to use previous method.
        for name, data in data.iteritems():
            self.write_output(name, data, tag=tag, timestamp=time_now)
        db.commit()


    def write_log(self, log_text, log_level=None):
        # Luca: Can you use the LogLevel.INFO defined
        """Writes a log message to the logs table
        param log_text : message to be logged
        param log_level : 0 for error, 1 for warning, 2 for info, 3 for debug """
        db = current.db
        log_level = slugiot_setup.LogLevel.INFO if log_level is None else log_level
        db.logs.insert(time_stamp=datetime.datetime.utcnow(),
                       modulename=self.procedure_name,
                       log_level=log_level,
                       log_message=log_text)
        db.commit()


    def add_schedule(self,
                     function,
                     function_args=[],
                     start_time=datetime.datetime.now(),
                     stop_time=None,
                     timeout=60,
                     period_between_runs=60,
                     repeats = 1,
                     num_retries=5):

        """Add a schedule to the Web2py scheduler.
        param function : The function in the procedure to be called when the schedule is triggered
        param function_args : list of arguments to be passed to the function
        param start_time : The time for the schedule to be assigned. datetime object. Passed to Web2py's queue_task
        param stop_time : datetime object, defaults to none.
        param timeout : The maximum time the function runs, defaults to 60 seconds
        param period_between_runs : The number of seconds between runs. Use this to setup a recurring schedule.
                             Defaults to 60 seconds
        param repeats : The number of times the task should run. Use this to setup a recurring schedule.
                            Defaults to 1, which means the function is run once
        param num_retries : The number of times a task is retried if it fails
        """
        from gluon import current
        current.slugiot_scheduler.queue_task(
            task_name=self.procedure_name + "_" + function,
            function='rerun_procedure',
            pvars = {'procedure':self.procedure_name, 'function':function, 'function_args':function_args},
            repeats = repeats,
            period = period_between_runs,
            start_time=start_time,
            stop_time=stop_time,
            timeout=timeout,
            retry_failed=num_retries)
        current.db.commit();


    def remove_all_schedules(self):
        """ Remove all schedules for the current procedure.
        """
        # TODO : Should we remove completed tasks ?
        # Luca: yes, you need some way to do cleanup of the table.
        self.write_log("Removing all scheduled tasks for the current procedure",
                       self.LogLevel.INFO)
        db = current.db
        db(db.scheduler_task.task_name.like(self.procedure_name + '_%')).delete()
        db.commit()

    def remove_schedule(self, function):
        """Deletes the existing schedule for this procedure and function
        param function: The function of this procedure whose schedule should be deleted"""

        # TODO : Should we remove completed tasks ?
        self.write_log("Removing scheduled task for the current function " + function,
                       self.LogLevel.INFO)
        db = current.db
        task_name = self.procedure_name + "_" + function
        db((db.scheduler_task.task_name == task_name) & (db.scheduler_task.status != 'COMPLETED')).delete()
        db.commit()