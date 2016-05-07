# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
import requests
from gluon import serializers
import slugiot_synchronization


def log_message():
    log_message = "Sample Message: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    if ('log_message' in request.vars):
        log_message = request.vars.log_message
    log_level = 3
    if ('log_level' in request.vars):
        log_level = int(request.vars.log_level)
    import procedureapi
    api = procedureapi.ProcedureApi("Synchronization")
    api.write_log(log_message, log_level)
    return response.json({"log_message" : log_message})


def add_output():
    output_value = datetime.utcnow()
    if ('output_value' in request.vars):
        output_value = request.vars.output_value
    output_key = "current_time"
    if ('output_key' in request.vars):
        output_key = int(request.vars.output_key)
    import procedureapi
    api = procedureapi.ProcedureApi("Synchronization")
    api.write_output(output_key, output_value)
    return response.json({"output_key" : output_key, "output_value" : output_value})





@request.restful()
def synchronize_logs():
    """
    This function syncs the information to the server. The data from  __get_log_data is serialized into JSON and posted on the server url = server_url + "/synchronization/receive_logs"
    and a 200 status code indicates successful posting of information and the synchronization_events time_stamps are updated or an error is sent in the response along with the time_stamp

       :return: Dictionary containing whether the request posted is a success or not and the latest synchronization time_stamp
       :rtype: Dictionary
    """
    def GET(*args, **vars):
        return response.json(slugiot_synchronization.get_data_for_synchronization(slugiot_setup, "logs"))
    def POST(*args, **vars):
        if (slugiot_synchronization.synchronize(slugiot_setup, "logs")):
            return "ok"
        else:
            return "failure"

    return locals()



@request.restful()
def synchronize_outputs():
    """
    This function syncs the information to the server. The data from  __get_log_data is serialized into JSON and posted on the server url = server_url + "/synchronization/receive_logs"
    and a 200 status code indicates successful posting of information and the synchronization_events time_stamps are updated or an error is sent in the response along with the time_stamp

       :return: Dictionary containing whether the request posted is a success or not and the latest synchronization time_stamp
       :rtype: Dictionary
    """
    def GET(*args, **vars):
        return response.json(slugiot_synchronization.get_data_for_synchronization(slugiot_setup, "outputs"))
    def POST(*args, **vars):
        if (slugiot_synchronization.synchronize(slugiot_setup, "outputs")):
            return "ok"
        else:
            return "failure"

    return locals()


# Adopted from procedureapi.py
def add_sync_schedule(self,
                      function,
                      start_time=datetime.utcnow(),
                      stop_time=None,
                      timeout=600,
                      period_between_runs=720,
                      repeats=1,
                      num_retries=5):

    """Add a schedule to the Web2py scheduler.
    param function : The function in the procedure to be called when the schedule is triggered.
    param function_args : list of arguments to be passed to the function.
    param start_time : The time for the schedule to be assigned. datetime object. Passed to Web2py's queue_task.
    param stop_time : datetime object, defaults to none.
    param timeout : The maximum time the function runs, defaults to 600 seconds.
    param period_between_runs : The number of seconds between runs. Use this to setup a recurring schedule.
                         Defaults to 720 seconds.
    param repeats : The number of times the task should run. Use this to setup a recurring schedule.
                        Defaults to 1, which means the function is run once.
    param num_retries : The number of times a task is retried if it fails. Defaults to 5 times.
    """
    from gluon import current

    current.slugiot_scheduler.queue_task(
        task_name=function,
        function='do_synchronization',
        pvars={'function': function},
        repeats=repeats,
        period=period_between_runs,
        start_time=start_time,
        stop_time=stop_time,
        timeout=timeout,
        retry_failed=num_retries)
    current.db.commit()


