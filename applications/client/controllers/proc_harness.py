#########################################################################
## Define API for interacting with procedure table
## These methods will be used in the controller, called by the code
## that actually performs the sync to interact with the tables
#########################################################################

import procedureapi as api
import json
from gluon import current
import os

import requests
db = current.db
proc_table = db.procedures
#settings_table = db.client_setting

def do_procedure_sync():
    """
    Perform sync of procedures according to the following protocol:
        Get all timestamps from server for last stable save of all procedures associated with this device
        Compare timestamps to timestamps retrieved at last synch and get new procedures
        Send list of procedure IDs that are needed from server
        Get updated data from server and save it to local database
    """

    # Luca: Why is this a controller?  I think it should be in a module.
    # Or perhaps in a model if you need to refer to it from a scheduler, but a module would be better.

    # Get device id from settings table - fix this based on Synch group code
    device_id = "1" #db().select(settings_table.device_id).first().device_id # Luca: get it from slugiot_setup

    # Get authorization from server for request???
    #   Waiting for other team to implement this method
    #   Not sure what to do here if anything
    # Luca: don't worry.  Just ask the server for any new procedures for a given device_id.

    # Request dictionary {procedure_id: last_updated_date} from server
    server_url = myconf.get('server.host')
    call_url = server_url + '/proc_harness/get_procedure_status/' + str(device_id)
    r = requests.get(call_url)
    # Luca: check r.status_code, and catch errors?
    server_status = r.json()

    # Luca: use logging
    print "server_status", server_status

    # Get corresponding dictionary from client procedure table
    client_status = get_procedure_status()

    print "proc status", client_status

    # Compare two dicts to get new procedures or procedures that have been updated
    synch_ids = compare_dates(server_status, client_status)

    if len(synch_ids) > 0:
        print "synch ids", synch_ids

        # Request full procedure data for new and updated procedures from server
        call_url_data = server_url + '/proc_harness/get_procedure_data/'
        call_url_names = server_url + '/proc_harness/get_procedure_names/'
        r = requests.get(call_url_data, params=json.dumps(synch_ids))

        synch_data = r.json()
        print "synch data", synch_data

        r = requests.get(call_url_names, params=json.dumps(synch_ids))
        synch_names = r.json()
        print "synch names", synch_names

        # Update local data
        insert_new_procedure(synch_data, synch_names, server_status)
        return "Status: Procedure Synch Complete"

    return "Status: No Procedure Synch Needed"

def get_procedure_status():
    """
    Returns full dictionary of format {procedure_id: last_updated_date} for all procedures on the client
    last_updated_date comes from server so can be directly compared to dates that come from server

    :return: Dict of the format {procedure_id: last_updated_date}
    :rtype:
    """

    # Get all procedure_ids for the device_id
    procedure_ids = db().select(proc_table.procedure_id)

    # Build dictionary containing last_update_stable date for each procedure_id
    procedure_info = {}
    for proc in procedure_ids:
        pid = proc.procedure_id
        procedure_info[pid] = db(proc_table.procedure_id == pid).select(proc_table.last_update).first().last_update

    return procedure_info


def insert_new_procedure(procedure_data, procedure_names, server_status):
    """
    Save all procedure code that has been fetched from the server
    Save original update date that comes from server - this may not correspond exactly to
        the last update date that is actually connected with this data on the server but it can't be later
        which is what matters for this synching process

    :param procedure_entries: Dict of the format {procedure_id: procedure_data}
    :type procedure_entries:
    :param server_status: Dict of the format {procedure_id: last_update_date}
    :type server_status:
    """

    print "INSIDE INSERT FUNCTION: "

    for proc, name in procedure_names.iteritems():
        data = procedure_data[proc]

        print proc, name, data, server_status[proc]

        # Storing procedure data as a file to avoid issues with exec
        # Luca: here you need to quote/validate name.  To e.g. rule out names that contain things
        # like ../.. and mess up the file system.  In general, it would be better to use str(procedure_id) here.
        file_name = "applications/client/modules/" + str(name) + ".py"
        with open(file_name, "wb") as procedure_file:
            procedure_file.write(data)

        # When procedures get updated old schedules should be removed so new schedules can be scheduled
        #api_obj = api.ProcedureApi(name)
        #api_obj.remove_all_schedules()
        #api_obj.add_schedule("run", repeats=1)

        proc_table.update_or_insert(procedure_id = proc,
                                    last_update = server_status[proc],
                                    name = name)

def compare_dates(server_dict, client_dict):
    """
    Determines which procedures need to be fetched from the server by comparing the last updated dates
        sent from the server to those on the client, and determining which procedures do not yet exist
        on the client

    :param server_dict: Dict of the format {procedure_id: last_updated_date} for procedures on server for this device
    :type server_dict:
    :param client_dict: Dict of the format {procedure_id: last_updated_date} for procedures on this device
    :type client_dict:
    :return: List of procedure_ids that should be fetched from the server
    :rtype:
    """

    synch_ids = []
    # Luca: so here you use procedure_id? ok
    for proc, date in server_dict.iteritems():
        if long(proc) not in client_dict:
            synch_ids.append(proc)
        else:
            if date != str(client_dict[long(proc)]):
                synch_ids.append(proc)

    return synch_ids