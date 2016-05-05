import os

from gluon import current
from gluon.admin import apath
from gluon.fileutils import read_file, write_file
from gluon.restricted import restricted


class SlugIOTSettings():

    DEVICE_ID_KEY = 'device_id'

    """
    These are generic methods for managing SlugIOT settings
    """
    def get_setting_value(self, setting_name, procedure_id=None, default_value=None):
        db = current.db
        value = db(db.settings.procedure_id == procedure_id).select(db.settings.setting_value, limitby=(0, 1))

        # there should only be one record (if any)
        for row in value:
            return row.setting_value
        # if there were no records
        return default_value

    def set_setting_value(self, setting_name, setting_value, procedure_id=None):
        db = current.db
        db.settings.update_or_insert(
            db.settings.setting_name == setting_name and db.settings.procedure_id == procedure_id,
            setting_name=setting_name, setting_value=setting_value, procedure_id=procedure_id)


    """
    These are accessors for global settings
    """

    def get_device_id(self):
        return self.get_setting_value(SlugIOTSettings.DEVICE_ID_KEY)

    def set_device_id(self, device_id):
        return self.set_setting_value(SlugIOTSettings.DEVICE_ID_KEY, device_id)


def check_device_id():
    """
    Check if device ID exists already

    :return: True if exists, False if not.
    :rtype: bool
    """
    settings_file = os.path.join(os.getcwd(),'device_settings.py')
    _config = {}

    # Check for the device settings file.
    # The file should be present only if a device ID has been added
    if os.path.isfile(settings_file):
        restricted(read_file(settings_file), _config)
        if not 'device_id' in _config or not _config['device_id']:
            return None
        else:
            return _config['device_id']
    else:
        return None

def set_device_id(entry=None):
    """
    Get the ID for device
    :return:
    :rtype:
    """
    settings_file = os.path.join(os.getcwd(),'device_settings.py')
    # if entry is not None:
    write_file(settings_file, entry)