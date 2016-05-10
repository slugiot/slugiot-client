#########################################################################
## Define API for interacting with procedure table
## These methods will be used in the controller, called by the code
## that actually performs the sync to interact with the tables
#########################################################################

import proc_harness_module as phm
from gluon import current
import logging
import requests
import sys

test_device_id = "test"
logger = logging.getLogger("web2py.app.client")
logger.setLevel(logging.INFO)

db = current.db
proc_table = db.procedures
#settings_table = db.client_setting

server_url = myconf.get('server.host')

def view_table():
    for row in db(proc_table).select():
        logger.debug(row)

def clear_tables():
    call_url = server_url + '/proc_harness_test/clear_tables'

    try:
        r = requests.get(call_url)
    except requests.exceptions.RequestException as e:
        logger.error(e)
        sys.exit(1)

    proc_table.truncate()

    if db(proc_table).isempty():
        logger.info("Client Table Cleared")
    return "Tables Cleared on Server and Client"

def new_proc_test():
    call_url = server_url + '/proc_harness_test/create_new_proc_for_synch'
    r = requests.get(call_url)

    phm.do_procedure_sync()

    view_table()

    return "New Procedure Test Complete"

def update_proc_test():
    call_url = server_url + '/proc_harness_test/update_proc_for_synch'
    r = requests.get(call_url)

    phm.do_procedure_sync()

    view_table()

    return "Update Procedure Test Complete"

def not_update_proc_test():
    call_url = server_url + '/proc_harness_test/update_proc_not_for_synch'
    r = requests.get(call_url)

    phm.do_procedure_sync()

    view_table()

    return "No Update Procedure Test Complete"

