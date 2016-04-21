# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World Sync")
    return dict(message=T('Welcome to web2py!'))

def test():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World Sync")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def test_log_message():
    log_message = request.vars.log_message
    log_level = request.vars.log_level
    import procedureapi
    api = procedureapi.ProcedureApi("Test")
    api.write_log(log_message, log_level)
    return response.json({"result" : "done"})

@request.restful()
def test_last_synchronized():
    table_name = "example"
    def GET(*args, **vars):
        return __get_last_synchronized(table_name)
    def POST(*args, **vars):
        return __set_last_synchronized(table_name, datetime.datetime.utcnow())
    return locals()

"""
This function takes in a table_name (logs, outputs, etc) and returns
the latest timestamp the data was synchronized
"""
def __get_last_synchronized(table_name):
    timestamp =  db(db.synchronization_events.table_name == table_name).select(db.synchronization_events.time_stamp, orderby="time_stamp DESC", limitby=(0, 1))
    if (not timestamp):
        return datetime.datetime.fromtimestamp(0)
    return timestamp[0].time_stamp

"""
This function takes in a table_name (logs, outputs, etc) and a timestamp
and inserts a record to store that it was updated.  The timestamp is NOT
defaulted to datetime.utcnow() because you need to store the timestamp
from when you retrieved the updates, so updates that occur during a sync
event are not lost
"""
def __set_last_synchronized(table_name, timestamp):
    db.synchronization_events.insert(table_name=table_name,time_stamp=timestamp)
