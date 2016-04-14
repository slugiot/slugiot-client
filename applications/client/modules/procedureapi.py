class ProcedureApi():

    def __init__(self, procedure_name):
        self.procedure_name = procedure_name

    def write_value(self, name, data):
        pass

    def write_output(self, name, data, tag):
        pass

    def write_log(self, log_text, log_level=0):
        pass

    # todo : schedule tasks for procedure
    def add_schedule(self):
        pass