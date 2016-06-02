import procedureapi
import json
from gluon import current
import sys
import requests
import logging
import os
from gluon.contrib.appconfig import AppConfig


def do_procedure_sync():
    """
    Perform sync of procedures according to the following protocol:
        Get all timestamps from server for last stable save of all procedures associated with this device
        Compare timestamps to timestamps retrieved at last synch and get new procedures
        Send list of procedure IDs that are needed from server
        Get updated data from server and save it to local database
    """
    logger = logging.getLogger("web2py.app.client")
    logger.setLevel(logging.INFO)

    myconf = AppConfig(reload=True)
    server_url = myconf.get('server.host')

    # Get device id from settings
    device_id = current.slugiot_setup.device_id

    # Request dictionary {procedure_id: last_updated_date} from server
    call_url = server_url + '/proc_harness/get_procedure_status/' + str(device_id)
    logger.info("call url: " + call_url)
    try:
        r = requests.get(call_url)
    except requests.exceptions.RequestException as e:
        logger.info(str(e))
        sys.exit(1)

    try:
        server_status = r.json()
    except:
        server_status = {}
    logger.debug("server_status: " + str(server_status))

    # Get corresponding dictionary from client procedure table
    client_status = get_procedure_status()
    logger.debug("proc status: " + str(client_status))

    # Compare two dicts to get new procedures or procedures that have been updated
    synch_ids = compare_dates(server_status, client_status)

    if len(synch_ids) > 0:
        logger.debug("synch ids: " + str(synch_ids))

        # Request full procedure data for new and updated procedures from server
        call_url_data = server_url + '/proc_harness/get_procedure_data/'
        call_url_names = server_url + '/proc_harness/get_procedure_names/'
        try:
            r = requests.get(call_url_data, params=json.dumps(synch_ids))
        except requests.exceptions.RequestException as e:
            logger.info(str(e))
            sys.exit(1)

        synch_data = r.json()
        logger.debug("synch data: " + str(synch_data))

        try:
            r = requests.get(call_url_names, params=json.dumps(synch_ids))
        except requests.exceptions.RequestException as e:
            logger.info(str(e))
            sys.exit(1)

        synch_names = r.json()
        logger.debug("synch names: " + str(synch_names))

        # Update local data
        insert_new_procedure(synch_data, synch_names, server_status)

def get_procedure_status():
    """
    Returns full dictionary of format {procedure_id: last_updated_date} for all procedures on the client
    last_updated_date comes from server so can be directly compared to dates that come from server

    :return: Dict of the format {procedure_id: last_updated_date}
    :rtype:
    """

    db = current.db
    proc_table = db.procedures

    if not db(proc_table).isempty():
        return {p.procedure_id: p.last_update for p in db(proc_table).select()}

    return {}


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

    db = current.db
    proc_table = db.procedures

    logger = logging.getLogger("web2py.app.client")
    logger.setLevel(logging.INFO)

    logger.debug("INSIDE INSERT FUNCTION")

    for proc in procedure_names.keys():
        data = procedure_data[proc]

        logger.debug(str(proc) + " " + str(proc) + " " + str(data) + " " + str(server_status[proc]))

        proc_directory = "applications/client/modules/procedures"
        init_file_name = os.path.join(proc_directory, "__init__.py")

        # Create procedure directory if it does not exist
        if not os.path.exists(proc_directory):
            os.makedirs(proc_directory)
            with open(init_file_name, "a"):
                os.utime(init_file_name, None)

        # Storing procedure data as a file
        file_name = os.path.join(proc_directory, proc)
        if file_name.find(".py") == -1:
            file_name = file_name + ".py"
        with open(file_name, "wb") as procedure_file:
            procedure_file.write(data)

        # When procedures get updated old schedules should be removed so new schedules can be scheduled
        api = procedureapi.ProcedureApi(proc)
        api.remove_schedule()
        api.add_schedule()

        logger.info("new schedule should be in place")

        proc_table.update_or_insert(proc_table.procedure_id == proc,
                                    procedure_id = proc,
                                    last_update = server_status[proc],
                                    name=proc)
        db.commit()

        logger.info("procedure table should be updated")

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
        if long(proc) not in client_dict:
            synch_ids.append(proc)
        else:
            if date != str(client_dict[long(proc)]):
                synch_ids.append(proc)

    return synch_ids


def enqueue_procedure_task(procedure):
    procedures = []
    if isinstance(procedure, list):
        procedures = procedure
    else:
        procedures.append(procedure)

    for proc in procedures:
        api = procedureapi.ProcedureApi(proc)
        api.add_schedule()

