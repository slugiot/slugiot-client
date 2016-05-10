import requests
import json_plus
from datetime import datetime
import urllib
from slugiot_setup import  LogLevel
import traceback
import threading

sync_lock = threading.Lock()


def synchronize(setup_info, table_name):
    """
    This function syncs the information in table_name to the corresponding server table.
    """
    with sync_lock:
        db = setup_info.db
        rows = db(db[table_name].time_stamp > _get_last_synchronized(db, table_name)).select(
            orderby=~db[table_name].time_stamp).as_dict()
        if len(rows) > 0:
            try:
                # Let's get the device id.
                # There is something to synch
                body = json_plus.Serializable.dumps(rows)
                url = (setup_info.server_url + "/synchronization/" +
                        urllib.quote(setup_info.device_id) + '/' +
                        urllib.quote(table_name)
                       )
                result = requests.post(url=url, data=body)
                if result.status_code == 200:
                    # Updates synch time.
                    _set_last_synchronized(db, table_name, rows[0]['timestamp'])
            except Exception, _:
                # We failed synch.  We write this to the logs.
                db.logs.insert(modulename=None, log_level = LogLevel.WARN,
                               log_message="Synch failed for logs: %s" % traceback.format_exc())
                return False
        return True


def synch_all(setup_info, tables):
    return all([synchronize(setup_info, t) for t in tables])


def _get_last_synchronized(db, table_name):
    row =  db(db.synchronization_events.table_name == table_name).select(
        db.synchronization_events.time_stamp, orderby=~db.synchronization_events.time_stamp).first()
    if row is None:
        return datetime.fromtimestamp(0)
    return row.time_stamp

def _set_last_synchronized(db, table_name, timestamp):
    """Updates the last synch time for table_name to timestamp"""
    db.synchronization_events.update_or_insert(
        db.synchronization_events.table_name == table_name,
        table_name = table_name,
        time_stamp=timestamp)


# Adopted from procedureapi.py
def add_sync_schedule(self,
                      function,
                      start_time=datetime.datetime.now(),
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


