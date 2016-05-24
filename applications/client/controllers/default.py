# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
import slugiot_settings


def _get_device_id():
    """
    Check for device ID being present.
    It makes two checks:
        1. Whether there's a setting called device_id or not
        2. Whether the setting device_id has any value or not
    :return:
    :rtype:
    """
    device_id_row = db(db.settings.setting_name == 'device_id').select().first()
    device_id = device_id_row.setting_value if device_id_row is not None else None
    return device_id


def index():
    """
    Index page for the client.

    Shows option to set/view a device ID based on whether the ID exists or not
    """
    # Check if settings exist already
    device_id = _get_device_id()
    return dict(device_id=device_id)


def settings():
    """
    Settings page for the device to set device ID.
    """
    device_id = _get_device_id()
    # If the device_id is None, we have to enter one.
    # Otherwise, we offer a form, which is view-only in general,
    # and can be turned into an edit form if needed.
    request_edit = request.vars.edit == 'y'
    is_edit = device_id is None or request_edit
    form = SQLFORM.factory(Field('device_id'), readonly=not is_edit)
    form.vars.device_id = device_id
    edit_button = None if is_edit else A("Edit", _href=URL('default', 'settings', vars={'edit': True}), _class='btn btn-primary')
    if form.process().accepted:
        db.settings.update_or_insert(db.settings.setting_name == 'device_id',
                                     setting_name='device_id',
                                     setting_value=form.vars.device_id)
        redirect(URL('default', 'index'))
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

