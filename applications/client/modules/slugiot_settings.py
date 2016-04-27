from gluon import current

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
