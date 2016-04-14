#########################################################################
## Define API for interacting with procedure table
## These methods will be used in the controller, called by the code
## that actually performs the sync to interact with the tables
#########################################################################

from gluon import current

proc_table = current.db["procedures"]

def insert_new_procedure(procedure_entry): #not exactly sure what the best way to do this is - pass in an entry from
    # whatever the server sends or pass in each entry besides sync time?
    pass

# something like this - we aren't sure how many versions of a procedure we want to keep around
# we might just keep the latest valid one but we might also need to get the latest one using the date
def get_latest_procedure(procedure_id):
    return db.proc_table(data, procedure_id==procedure_id, valid==True)

# the functionality of this will depend on how many versions we want to keep around
def cleanup_procedure_table(procedure_id):
    pass