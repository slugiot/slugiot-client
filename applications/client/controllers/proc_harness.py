#########################################################################
## Define API for interacting with procedure table
## These methods will be used in the controller, called by the code
## that actually performs the sync to interact with the tables
#########################################################################

from gluon import current

proc_table = db["procedure"]
device_table = db["device"]

def do_procedure_sync():
    # 1. Get device id from settings table ?? How do we know what device we are on
    device_id = db().select(device_table.id)
    # 2. Get authorization from server for request
    #   Waiting for other team to implement this method
    # 3. Request dictionary (of procedure ids and dates) from server
    server_status = 'http://127.0.0.1:8080/proc_harness/get_procedure_status(device_id)'
    # 4. Get corresponding dictionary of proc ids and dates from client procedure table
    client_status = get_procedure_status()
    # 5. Compare dates by LOOPING through (don't ignore new procs that aren't in client table!)
    synch_ids = compare_dates(server_status, client_status)
    # 6. Request full proceudure data for new and newer procs from server; convert to JSON format
    synch_data = 'http://127.0.0.1:8080/proc_harness/get_procedure_update(synch_ids).json'
    # 8. Use JSON file as param in function call to update procedures on client
    insert_new_procedure(synch_data)
    pass

# called to get data from client to compare with dictionary data returned by server
# assumes that only procs owned by client are stored within client.procedure table.
# returns a dictionary of the format {procedure_id, last_update}
def get_procedure_status():
    # 1. Get all procedure_ids for the device_id
    procedure_ids = db().select(proc_table.procedure_id)
    # 2. build dictionary containing last_update_stable date for each procedure_id
    procedure_info = {}
    for proc in procedure_ids:
        procedure_info[proc.procedure_id] = get_procedure_data(proc, True)
    # 3. return dictionary
    return procedure_info

# Pulls proc data from procedure table
def get_procedure_data(procedure_id):
    #max = proc_table.last_update.max()
    #date = db(proc_table.procedure_id == procedure_id).select(max).first()[max]
    return db(proc_table.procedure_id == procedure_id).select(proc_table.procedure_data).first().procedure_data

def insert_new_procedure(procedure_entries): #not exactly sure what the best way to do this is - pass in an entry from
    # whatever the server sends or pass in each entry besides sync time?
    # Need to loop through json data passed as parameter and call on each:
    proc_table.update_or_insert(procedure_id=proc_id,
                                     user_id=user_id,
                                     last_name=last_update,
                                     proc_name=proc_name,
                                     proc_data=proc_data
                                     )

# something like this - we aren't sure how many versions of a procedure we want to keep around
# we might just keep the latest valid one but we might also need to get the latest one using the date
def compare_dates(server_dict, client_dict):
    # returns bool that determines if procedures needs to be synced
    # for item in server_status ...
    #return db.proc_table(data, procedure_id==procedure_id, valid==True)
    pass

# the functionality of this will depend on how many versions we want to keep around
def cleanup_procedure_table(procedure_id):
    pass