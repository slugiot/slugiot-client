import unittest

from selenium import webdriver
import time
from subprocess import Popen, PIPE
demo_time = 2

class ProcHarnessTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        # launch client
        c_fd = open("../logs/client_log.txt","w")
        s_fd = open("../logs/server_log.txt","w")
        p_c = Popen("../web2py.py -p 7999 -a blah", shell=True, universal_newlines=True, stderr=c_fd)
        p_s = Popen("../web2py.py -p 8000 -a blah", shell=True, universal_newlines=True, stderr=s_fd)
        self.pid_c = p_c.pid
        self.pid_s = p_s.pid
        
    def test_clear_tables(self):
        self.driver.get('http://127.0.0.1:7999/test_proc_harness/clear_tables')

    #def test_new_proc(self):
    #    self.driver.get('http://127.0.0.1:7999/test_proc_harness/new_proc_test')
    #    time.sleep(demo_time)

    #def test_update_proc(self):
    #    self.driver.get('http://127.0.0.1:7999/test_proc_harness/update_proc_test')

    #def test_no_update_proc(self):
    #    self.driver.get('http://127.0.0.1:7999/test_proc_harness/not_update_proc_test')

    def tearDown(self):
        Popen(["kill", "-SIGTERM", str(self.pid_c)])
        Popen(["kill", "-SIGTERM", str(self.pid_s)])
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()