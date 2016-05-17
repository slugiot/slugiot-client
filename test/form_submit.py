import unittest
from selenium import webdriver
from urlparse import urlparse
import time
import os
import urllib

# Get the current directory
current_dir = os.getcwd()

# Encode the url: replace spaces with %20
local_url = 'file://' + urllib.quote(current_dir + '/example_pages/form.html')
demo_time = 2

class SeleniumTest(unittest.TestCase):

    # This is called before each test
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get(local_url) #load local file into browser

        # Get the input elements by id
        # They are here because they are all required for each test
        self.username = self.driver.find_element_by_id('name')
        self.email = self.driver.find_element_by_id('email')
        self.password = self.driver.find_element_by_id('password')
        self.password_confirm = self.driver.find_element_by_id('confirm')
        self.submit_button = self.driver.find_element_by_id('submit')


    def test_no_username(self):

        self.email.send_keys("Johndoe@slugiot.com") # Write to input filed
        time.sleep(demo_time)  # For demo purpose

        self.password.send_keys("12345abc")
        time.sleep(demo_time)

        self.password_confirm.send_keys("12345abc")
        time.sleep(demo_time)

        self.submit_button.click()
        time.sleep(demo_time)

        error = self.driver.find_element_by_class_name("error") # Find all labels with error
        error = error.find_element_by_xpath("//label[@for='name']") # Filter out the one that is for name

        # make sure we are still on the same page, since form contains errors
        self.assertEqual(local_url, self.driver.current_url)

        # make sure the error label has correct message
        self.assertEqual("This field is required.", error.text)

    def test_invalid_email(self):

        self.username.send_keys("Johndoe Doe")

        self.email.send_keys("Johndoe@")
        time.sleep(demo_time)

        self.password.send_keys("12345abc")
        time.sleep(demo_time)

        self.password_confirm.send_keys("12345abc")
        time.sleep(demo_time)

        self.submit_button.click()
        time.sleep(demo_time)

        error = self.driver.find_element_by_class_name("error")
        error = error.find_element_by_xpath("//label[@for='email']")

        self.assertEqual(local_url, self.driver.current_url)
        self.assertEqual("Please enter a valid email address.", error.text)


    def test_invalid_password(self):

        self.username.send_keys("Johndoe Doe")

        self.email.send_keys("johndoe@slugiot.com")
        time.sleep(demo_time)

        self.password.send_keys("1234")
        time.sleep(demo_time)

        self.password_confirm.send_keys("1234")
        time.sleep(demo_time)

        self.submit_button.click()
        time.sleep(demo_time)

        error = self.driver.find_element_by_class_name("error")
        error = error.find_element_by_xpath("//label[@for='password']")

        self.assertEqual(local_url, self.driver.current_url)
        self.assertEqual("Please enter at least 5 characters.", error.text)

    def test_unmatch_confirmation(self):

        self.username.send_keys("Johndoe Doe")

        self.email.send_keys("johndoe@slugiot.com")
        time.sleep(demo_time)

        self.password.send_keys("12345abc")
        time.sleep(demo_time)

        self.password_confirm.send_keys("12345")
        time.sleep(demo_time)

        self.submit_button.click()
        time.sleep(demo_time)

        error = self.driver.find_element_by_class_name("error")
        error = error.find_element_by_xpath("//label[@for='confirm']")

        self.assertEqual(local_url, self.driver.current_url)
        self.assertEqual("Please enter the same value again.", error.text)


    # test success scenario
    def test_success(self):
        self.username.send_keys("John Doe")
        time.sleep(demo_time) #sleep for 2 seconds for demoing purpose, otherwise it is too fast

        self.email.send_keys("Johndoe@slugiot.com")
        time.sleep(demo_time)

        self.password.send_keys("12345abc")
        time.sleep(demo_time)

        self.password_confirm.send_keys("12345abc")
        time.sleep(demo_time)

        self.submit_button.click()
        time.sleep(demo_time)
        body = self.driver.find_element_by_tag_name("body")

        self.assertEqual('http://requestb.in/q6bf4yq6', self.driver.current_url)
        self.assertEqual('ok', body.text)

    # This is called after each test
    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()