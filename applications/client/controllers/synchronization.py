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


def test_log_message():
    log_message = request.vars.log_message
    log_level = request.vars.log_level
    import procedureapi
    api = procedureapi.ProcedureApi("Test")
    api.write_log(log_message, log_level)
    return response.json({"result" : "done"})

def writing_to_db():
    current.db.logs.insert(time_stamp=datetime.utcnow(),modulename="Test",log_level=0,log_message="Writing to database0")
    current.db.logs.insert(time_stamp=datetime.utcnow(), modulename="Test", log_level=0,log_message="Writing to database1")
    current.db.logs.insert(time_stamp=datetime.utcnow(), modulename="Test", log_level=0,log_message="Writing to database2")
    return response.json({"result": "done"})

def reading_from_db(table_name_db,time_to_sync):
    for row in db(db.table_name == table_name).iterselect(db.table_name):
        print row.log_message,row.time_stamp

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
This function takes in a table_name (logs, outputs, etc) and a timestamp
and inserts a record to store that it was updated.  The timestamp is NOT
defaulted to datetime.utcnow() because you need to store the timestamp
from when you retrieved the updates, so updates that occur during a sync
event are not lost
"""
def __set_last_synchronized(table_name, timestamp):
    db.synchronization_events.insert(table_name=table_name,time_stamp=timestamp)

