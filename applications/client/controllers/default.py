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
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


@request.restful()
def initialization():

    def GET(*args, **vars):
        if (server_url == None):
            return "Please configure your server_url field in applications/private/appconfig.ini"
        device_id = __get_setting_value("device_id")
        if (device_id == None):
            return "Please POST to this url the desired identifier for your device with the 'device_id' parameter"
        return "Your device_id is: " + device_id

    def POST(*args, **vars):
        if (vars == None or not vars.has_key('device_id')):
            return "Please POST to this url the desired identifier for your device with the 'device_id' parameter"
        device_id = vars['device_id']
        __set_setting_value("device_id", device_id)
        return "Your device_id has been set to: " + device_id

    return locals()




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

def __get_setting_value(setting_name, procedure_id=None, default_value=None):
    value = db(db.settings.procedure_id == procedure_id).select(db.settings.setting_value, limitby=(0, 1))

    # there should only be one record (if any)
    for row in value:
        return row.setting_value
    # if there were no records
    return default_value


def __set_setting_value(setting_name, setting_value, procedure_id=None):
    db.settings.update_or_insert(db.settings.setting_name == setting_name and db.settings.procedure_id == procedure_id,
                                 setting_name=setting_name,setting_value=setting_value,procedure_id=procedure_id)