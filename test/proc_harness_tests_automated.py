import unittest
from selenium import webdriver
import time
import os
from pdb import set_trace
from subprocess import Popen, PIPE
demo_time = 60

class ProcHarnessTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

        normalizedPath_c = os.path.abspath(os.getcwd() + "/../logs/client_log.txt")
        normalizedPath_s = os.path.abspath(os.getcwd() + "/../logs/server_log.txt")
        normalizedPath = os.path.abspath(os.getcwd() + "/../web2py.py")

        self.client_log = open(normalizedPath_c, "r")
        self.server_log = open(normalizedPath_s, "r")

        p_c = Popen("python " + normalizedPath + " -p 7999 -a blah 2>> " + normalizedPath_c + " 1>>/dev/null", shell=True)
        p_s = Popen("python " + normalizedPath + " -p 8000 -a blah 2>> " + normalizedPath_s + " 1>>/dev/null", shell=True)

        self.pid_c = p_c.pid
        self.pid_s = p_s.pid

        self.client_test_url = 'http://127.0.0.1:7999/test_proc_harness'
        self.proc_dir = os.path.abspath(os.getcwd() + "/../applications/client/modules/")

    def test_clear_tables(self):
        server = False
        client = False
        self.driver.get(self.client_test_url + '/clear_tables')

        for line in self.server_log.xreadlines():
            if line.find("Server Table Cleared") != -1:
                server = True

        for line in self.client_log.xreadlines():
            if line.find("Client Table Cleared") != -1:
                client = True

        self.assertTrue(server & client)

    def test_new_proc(self):
        new_proc = False
        self.driver.get(self.client_test_url + '/new_proc_test')

        for line in self.server_log.xreadlines():
            if line.find("look for proc_id and name:") != -1:
                pieces = line.split()
                new_proc_name = pieces[6]
                dir_items = os.listdir(self.proc_dir)
                if new_proc_name + ".py" in dir_items:
                    new_proc = True

        self.assertTrue(new_proc)

    def test_update_proc(self):
        update_proc = False

        self.driver.get(self.client_test_url + '/update_proc_test')

        for line in self.server_log.xreadlines():
            if line.find("look for proc_id, name, data") != -1:
                pieces = line.split()
                proc_name = pieces[7]
                data = pieces[8]

                with open(self.proc_dir + "/" + proc_name + ".py") as file:
                    for line in file.readlines():
                        if line.find(data) != -1:
                            update_proc = True

        self.assertTrue(update_proc)

    def test_no_update_proc(self):
        no_update_proc = False

        self.driver.get(self.client_test_url + '/not_update_proc_test')

        for line in self.server_log.xreadlines():
            if line.find("should not see data") != -1:
                pieces = line.split()
                proc_name = pieces[10]
                data = pieces[5]

                with open(self.proc_dir + "/" + proc_name + ".py") as file:
                    for line in file.readlines():
                        if line.find(data) != -1:
                            no_update_proc = True

        self.assertFalse(no_update_proc)

    def tearDown(self):
        Popen(["kill", "-SIGTERM", str(self.pid_c)])
        Popen(["kill", "-SIGTERM", str(self.pid_s)])

        self.driver.quit()
        self.client_log.close()
        self.server_log.close()

if __name__ == '__main__':
    unittest.main()