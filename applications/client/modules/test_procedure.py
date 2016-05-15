# This is a test procedure file. It interacts with slugIOT through procedureapi
from procedureapi import Procedure
import logging
logger=logging.getLogger()

class DeviceProdecure(Procedure):

    def init(self):
        self.x = 0
        # Runs for 10 days, once per day.
        self.api.add_schedule(delay=10, class_name='DeviceProdecure', repeats=10, period_between_runs=86400)

    def run(self):
        self.api.log_info("Look at me!  I am running! x = %d" % self.x)
        self.x += 1
