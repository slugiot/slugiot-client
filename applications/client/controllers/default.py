# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
import slugiot_settings


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello")

    # Check if settings exist already
    if not slugiot_settings.check_device_id():
        message = T('Welcome to SlugIOT Client. Please register device')
        settings = A("Click here to initialize your device", _href=URL('default','settings',vars={'new':True}), _class = 'btn btn-primary')
    else:
        message = T('This device is registered')
        settings = A("Click here to see/edit device settings", _href=URL('default','settings'), _class = 'btn btn-success')
    return dict(message=message, settings =settings)


def settings():
    """
    Settings page for the device to set device ID.
    """
    # Get device ID
    device_id = slugiot_settings.check_device_id() if slugiot_settings.check_device_id() is not None else ""
    settings_dict = dict(device_id=device_id)

    # For edit option
    if request.vars.new or request.vars.edit:
        form = SQLFORM.dictform(settings_dict)
        edit_button = T("")
        if form.process().accepted:
            settings_dict.update(form.vars)
            slugiot_settings.set_device_id("device_id=%r"%(settings_dict['device_id']))
            redirect(URL('default','index'))

    # For view option
    else:
        form = H2("Device ID: ",str(device_id))
        edit_button = A("Edit", _href=URL('default', 'settings',vars={'edit':True}), _class = 'btn btn-primary')

    return dict(form=form, edit_button=edit_button)

@request.restful()
def initialization():
    """
    This endpoint is used to manage the initialization of the client's
    device_id.  Making a GET request should detail either what the
    device_id is, or how to set it.  Making a POST request is how it
    is actually set.

    Currently, this does not actually call the server to set the value,
    but that shouldn't be too difficult to manage.

    tpesout: I don't know how to set up a web2py form.  Maybe someone
    else can do that and use the functionality I added here to actually
    do it?
    """
    if (server_url == None):
        return "Please configure your server_url field in applications/private/appconfig.ini"

    def GET(*args, **vars):
        device_id = settings.get_device_id()
        if (device_id == None):
            return "Please POST to this url the desired identifier for your device with the 'device_id' parameter"
        return "Your device_id is: " + device_id

    def POST(*args, **vars):
        if (vars == None or not vars.has_key('device_id')):
            return "Please POST to this url the desired identifier for your device with the 'device_id' parameter"
        device_id = vars['device_id']
        settings.set_device_id(device_id)
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

