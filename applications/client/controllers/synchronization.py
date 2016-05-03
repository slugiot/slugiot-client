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

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World Sync")
    return dict(message=T('Welcome to web2py!'))

"""
This function syncs the information to the server. The data from  __get_log_data is serialized into JSON and posted on the server url = server_url + "/synchronization/receive_logs"
and a 200 status code indicates successful posting of information and the synchronization_events time_stamps are updated or an error is sent in the response along with the time_stamp

   :return: Dictionary containing whether the request posted is a success or not and the latest synchronization time_stamp
   :rtype: Dictionary
"""
@request.restful()
def synchronize_logs():
    synchronized_timestamp = datetime.utcnow()
    data = __get_log_data(synchronized_timestamp)
    def GET(*args, **vars):
        return response.json(data)
    def POST(*args, **vars):
        url = server_url + "/synchronization/receive_logs"
        json_data = serializers.json(data)
        sync_response = requests.post(url=url, data=json_data)
        if (sync_response.status_code == 200):
            #success
            __set_last_synchronized("logs", synchronized_timestamp)
            return response.json(
                dict(success=True,timestamp=synchronized_timestamp))
        else:
            #failure
            error = sync_response.content
            return response.json(
                dict(
                    success=False,
                    timestamp=synchronized_timestamp,
                    error=error,
                    server_url=url,
                )
            )

    return locals()


"""
This function gets the values from the "logs" table. It returns as a dictionary all values greater than the latest timestamp in the synchronization_events
table and all values lesser than the paramter current_timestamp. This allows for all the values on client but not on server to be stored in a dictionary
ready to be sycnhed.

   :param p1: current_timestamp
   :type p1: str
   :return: dictionary of all values in the logs table > synchronization_events.time_stamp and < current_timestamp
   :rtype: dictionary
"""

def __get_log_data(current_timestamp):
    log_db_data = db(db.logs.time_stamp >= __get_last_synchronized("logs")
                     and db.logs.time_stamp < current_timestamp
                     ).select()
    return dict(
        device_id=settings.get_device_id(),
        logs=log_db_data
    )

"""
This function takes in a table_name (logs, outputs, etc) and returns the latest timestamp the data was synchronized

   :param p1: table_name
   :type p1: str
   :return: Timestamp of latest entry in a database table
   :rtype: datetime
"""

def __get_last_synchronized(table_name):
    timestamp =  db(db.synchronization_events.table_name == table_name).select(db.synchronization_events.time_stamp, orderby="time_stamp DESC", limitby=(0, 1))
    if (not timestamp):
        return datetime.fromtimestamp(0)
    return timestamp[0].time_stamp

"""
This function takes in a table_name and timestamp and inserts in into the synchronization_events table

   :param p1: table_name
   :type p1: str
   :param p1: timestamp
   :type p1: str
"""

def __set_last_synchronized(table_name, timestamp):
    db.synchronization_events.insert(table_name=table_name,time_stamp=timestamp)

