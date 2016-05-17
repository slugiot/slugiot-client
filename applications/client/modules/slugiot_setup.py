import json_plus

class SlugIOTSetup(json_plus.Storage):
    """This class acts as container for a number of slugiot paramters.
    You can do:
    s = SlogIOTSetup()
    s.blah = 6
    t = s.blah + 1
    """
    def __init__(self):
        self.device_id = None
        self.db = None
        self.server_url = None

class LogLevel(object):
    CRITICAL = 0
    ERROR = 1
    WARN = 2
    INFO = 3
    DEBUG = 4
