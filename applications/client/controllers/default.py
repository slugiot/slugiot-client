# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
import slugiot_settings


def _device_id_exists():
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
    return True if device_id is not None else False


def index():
    """
    Index page for the client.

    Shows option to set/view a device ID based on whether the ID exists or not
    """
    # Check if settings exist already
    if not _device_id_exists():
        message = T('Welcome to SlugIOT Client. Please register device')
        settings = A("Click here to initialize your device", _href=URL('default', 'settings', vars={'new': True}),
                     _class='btn btn-primary')
    else:
        message = T('This device is registered')
        settings = A("Click here to see/edit device settings", _href=URL('default', 'settings'),
                     _class='btn btn-success')
    return dict(message=message, settings=settings)


def settings():
    """
    Settings page for the device to set device ID.
    """
    device_id_row = db(db.settings.setting_name == 'device_id').select().first()
    device_id = device_id_row.setting_value if device_id_row is not None else None

    # For new or edit option
    if request.vars.new or request.vars.edit:
        form = SQLFORM.factory(Field('device_id'))
        edit_button = T("")
        if device_id is not None:
            form.vars.device_id = device_id

        if form.process().accepted:
            db.settings.update_or_insert(db.settings.setting_name == 'device_id',
                                         setting_name='device_id',
                                         setting_value=form.vars.device_id)

            redirect(URL('default', 'index'))

    # For view option
    else:
        form = H2("Device ID: ", str(device_id))
        edit_button = A("Edit", _href=URL('default', 'settings', vars={'edit': True}), _class='btn btn-primary')

    return dict(form=form, edit_button=edit_button)


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
