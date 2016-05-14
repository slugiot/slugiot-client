import json_plus
import json
import urllib
from slugiot_setup import  LogLevel
import traceback
import threading
from datetime import datetime;
import requests

sync_lock = threading.Lock()



def synchronize(setup_info, table_name):
    """
    This function syncs the information in table_name to the corresponding server table.
    """
    with sync_lock:
        db = setup_info.db
        rows = get_data_for_synchronization(setup_info, table_name)
        if len(rows) > 0:
            try:
                # Let's get the device id.
                # There is something to synch
                data = dict(device_id=setup_info.device_id)
                data[table_name] = rows
                body = json_plus.Serializable.dumps(data)
                url = (setup_info.server_url + "/synchronization/receive_" +
                       urllib.quote(table_name)
                       )
                result = requests.post(url=url, data=body)
                if result.status_code == 200:
                    # Updates synch time.
                    set_last_synchronized(db, table_name, rows[0]['time_stamp'])
                    return True
                db.logs.insert(procedure_id=None, log_level=LogLevel.WARN,
                               log_message="Synch failed for logs: %s" % result.content)

            except Exception, _:
                # We failed synch.  We write this to the logs.
                db.logs.insert(procedure_id=None, log_level = LogLevel.WARN,
                               log_message="Synch failed for logs: %s" % traceback.format_exc())

            return False
        return True

def get_data_for_synchronization(setup_info, table_name):
    db = setup_info.db
    return db(db[table_name].time_stamp > get_last_synchronized(db, table_name)).select(
        orderby=~db[table_name].time_stamp).as_list()


def synch_all(setup_info, tables=["logs", "outputs"]):
    return all([synchronize(setup_info, t) for t in tables])


def get_last_synchronized(db, table_name):
    row =  db(db.synchronization_events.table_name == table_name).select(
        db.synchronization_events.time_stamp, orderby=~db.synchronization_events.time_stamp).first()
    if row is None:
        return datetime.fromtimestamp(0)
    return row.time_stamp

def set_last_synchronized(db, table_name, timestamp):
    """Updates the last synch time for table_name to timestamp"""
    db.synchronization_events.update_or_insert(
        db.synchronization_events.table_name == table_name,
        table_name = table_name,
        time_stamp=timestamp)


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
    # NOTE: we have to first check that there are no other
    # occurrences of these schedules in the db.

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

def synchronize_settings(setup_info):
        # get device id
        # get last synchronized time for 'settings' table
        db = setup_info.db
        synchronize_time = get_last_synchronized(db, 'settings')
        body = dict(device_id=setup_info.device_id, last_updated=synchronize_time)  # , last_updated = synchronize_time)
        # make call to server at /synchronize
        url = (setup_info.server_url + "/synchronization/get_settings")
        result = requests.get(url=url, params=body)
        if (not result):
            return True
        # returns error when we need to parse the setting information to python object/
        data = json_plus.Serializable.loads(result.content)
        # parse setting information (    json_plus.Serializable.loads)
        try:
            # pass settings to save_settings
            # if success, return true, else return false
            save_settings(setup_info, data)
            return True
        except Exception, _:
            # We failed synch.  We write this to the logs.
            db.logs.insert(procedure_id=None, log_level=LogLevel.WARN,
                           log_message="Synch failed for settings: %s" % traceback.format_exc())
        return False


def save_settings(setup_info, setting_data):
    """
    This function receives the setting information and saves it
    """

    db = setup_info.db
    settings = setup_info.settings
    synchronize_time = get_last_synchronized(db, 'settings')

    try:
        # we use setup_info.settings (from SlugIOTSettings object)
        for setting in setting_data:
            settings.set_setting_value(setting['setting_name'], setting['setting_value'], setting['procedure_id'])
            # getting last updated time
            # if ('last_updated' in setting and isinstance(setting['last_updated'], datetime) and setting['last_updated'] > synchronize_time):
            if (setting['last_updated'] > synchronize_time):
                synchronize_time = setting['last_updated']

        return True
    except Exception, _:
        # We failed synch.  We write this to the logs.
        db.logs.insert(procedure_id=None, log_level=LogLevel.WARN,
                       log_message="Synch failed for settings: %s" % traceback.format_exc())

    return False
