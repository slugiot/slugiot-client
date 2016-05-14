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


def set_value():
    key = "synchronization_example"
    if ('key' in request.vars):
        key = request.vars.key
    value = datetime.utcnow()
    if ('value' in request.vars):
        value = request.vars.value
    values = dict()
    values[key] = value
    import procedureapi
    api = procedureapi.ProcedureApi("Synchronization")
    api.write_value(values)
    return response.json({"values":values})





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
        if (slugiot_synchronization.synchronize_c2s(slugiot_setup, "logs")):
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
        if (slugiot_synchronization.synchronize_c2s(slugiot_setup, "outputs")):
            return "ok"
        else:
            return "failure"

    return locals()


@request.restful()
def synchronize_module_values():
    """
    This function syncs the information to the server. The data from  __get_log_data is serialized into JSON and posted on the server url = server_url + "/synchronization/receive_logs"
    and a 200 status code indicates successful posting of information and the synchronization_events time_stamps are updated or an error is sent in the response along with the time_stamp

       :return: Dictionary containing whether the request posted is a success or not and the latest synchronization time_stamp
       :rtype: Dictionary
    """
    def GET(*args, **vars):
        return response.json(slugiot_synchronization.get_data_for_synchronization(slugiot_setup, "module_values"))
    def POST(*args, **vars):
        if (slugiot_synchronization.synchronize_c2s(slugiot_setup, "module_values")):
            return "ok"
        else:
            return "failure"

    return locals()


@request.restful()
def synchronize_settings():
    """
    This function retrieves setting data from the server based on a timestamp (of last sync) and device_id.
    If there are changes, it applies them to the client's settings.
    """

    def GET(*args, **vars):
        return response.json(settings.get_all_settings())

    def POST(*args, **vars):
        if (slugiot_synchronization.synchronize_settings(slugiot_setup)):
            return "ok"
        else:
            return "failure"

    return locals()

