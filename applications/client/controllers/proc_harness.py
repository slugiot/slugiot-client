#########################################################################
## Define API for interacting with procedure table
## These methods will be used in the controller, called by the code
## that actually performs the sync to interact with the tables
#########################################################################

from gluon import current

import requests
import json

proc_table = db.procedure
settings_table = db.client_setting

def do_procedure_sync():
    """
    Perform sync of procedures according to the following protocol:
        Get all timestamps from server for last stable save of all procedures associated with this device
        Compare timestamps to timestamps retrieved at last synch and get new procedures
        Send list of procedure IDs that are needed from server
        Get updated data from server and save it to local database
    """

    # Get device id from settings table
    device_id = db().select(settings_table.device_id).first().device_id

    # Get authorization from server for request???
    #   Waiting for other team to implement this method
    #   Not sure what to do here if anything

    # Request dictionary {procedure_id: last_updated_date} from server
    server_url = myconf.get('server.host')
    call_url = server_url + '/proc_harness/get_procedure_status(' + str(device_id) + ').json'
    server_status = json.loads(requests.get(call_url))

    # Get corresponding dictionary from client procedure table
    client_status = get_procedure_status()

    # Compare two dicts to get new procedures or procedures that have been updated
    synch_ids = compare_dates(server_status, client_status)

    # Request full procedure data for new and updated procedures from server
    call_url = server_url + '/proc_harness/get_procedure_update(' + json.dumps(synch_ids) + '.json'
    synch_data = json.loads(requests.get(call_url))

    # Update local data
    insert_new_procedure(synch_data)


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


def insert_new_procedure(procedure_entries, server_status):
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

    for proc, data in procedure_entries.iteritems():
        proc_table.update_or_insert(procedure_id = proc,
                                    procedure_data = data,
                                    last_update = server_status[proc])


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
    for proc, date in server_dict.iteritems():
        if proc not in client_dict:
            synch_ids.append(proc)
        else:
            if date < client_dict[proc]:
                synch_ids.append(proc)

    return synch_ids