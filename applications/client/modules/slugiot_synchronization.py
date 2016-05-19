import json_plus
import urllib
from slugiot_setup import  LogLevel
import traceback
import threading
from datetime import datetime;
import requests
from dateutil.parser import parse as parse_date
import proc_harness_module

sync_lock = threading.Lock()


def synch_all_c2s(setup_info, tables=["logs", "outputs", "module_values"]):
    return all([synchronize_c2s(setup_info, t) for t in tables])

def synchronize_c2s(setup_info, table_name):
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
    # returns error when we need to parse the setting information to python objec
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
        procedures = []
        for setting in setting_data:
            procedure = setting['procedure_id']
            if not procedure in procedures:
                procedures.append(procedure)

            settings.set_setting_value(setting['setting_name'], setting['setting_value'], procedure)
            # getting last updated time
            last_updated = setting['last_updated']
            last_updated_datetime = last_updated
            if (not isinstance(last_updated, datetime)):
                last_updated_datetime = parse_date(last_updated)

            if ( last_updated_datetime > synchronize_time):
                synchronize_time = last_updated_datetime

        set_last_synchronized(db, 'settings', synchronize_time)
        if (len(procedures > 0)):
            proc_harness_module.enqueue_procedure_task(procedures)

        return True
    except Exception, _:
        # We failed synch.  We write this to the logs.
        db.logs.insert(procedure_id=None, log_level=LogLevel.WARN,
                       log_message="Synch failed for settings: %s" % traceback.format_exc())

    return False
