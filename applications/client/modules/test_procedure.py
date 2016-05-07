# This is a test procedure file. It interacts with slugIOT through procedureapi
from procedureapi import Procedure

class TestProcedure(Procedure):

    def init(self):
        self.x = 0

    def run(self):
        self.api.log_info("Look at me!  I am running! x = %d" % x)
        self.api.add_schedule(delay=30)
        self.x += 1
