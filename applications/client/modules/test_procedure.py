# This is a test procedure file. It interacts with slugIOT through procedureapi
from procedureapi import Procedure
import logging
logger=logging.getLogger()

class TestProcedure(Procedure):

    def init(self):
        self.x = 0

    def run(self):
        self.api.log_info("Look at me!  I am running! x = %d" % self.x)
        logger.error("Look at me!  I am running! x = %d" % self.x)
        self.api.add_schedule(delay=10, class_name='TestProcedure')
        self.x += 1
