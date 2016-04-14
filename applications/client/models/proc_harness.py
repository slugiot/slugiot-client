#########################################################################
## Define API for interacting with procedure table
## These methods will be used in the controller, called by the code
## that actually performs the sync to interact with the tables
#########################################################################

from gluon import current

proc_table = current.db["procedures"]

def do_procedure_sync():
    # 1. Get device id from settings table ?? How do we know what device we are on
    # 2. Request dictionary from server
    # 3. Compare dates
    pass

def insert_new_procedure(procedure_entry): #not exactly sure what the best way to do this is - pass in an entry from
    # whatever the server sends or pass in each entry besides sync time?
    pass

# something like this - we aren't sure how many versions of a procedure we want to keep around
# we might just keep the latest valid one but we might also need to get the latest one using the date
def compare_dates(procedure_id, date_from_server):
    # returns bool that determines if procedures needs to be synced
    #return db.proc_table(data, procedure_id==procedure_id, valid==True)
    pass

# the functionality of this will depend on how many versions we want to keep around
def cleanup_procedure_table(procedure_id):
    pass