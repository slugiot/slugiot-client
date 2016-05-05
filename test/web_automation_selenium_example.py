import unittest

from selenium import webdriver
from urlparse import urlparse
import time
demo_time = 2



class SeleniumTest(unittest.TestCase):

    # This is called before each test
    def setUp(self):
        self.driver = webdriver.Firefox()

    # test log in page redirect to google
    def test_login(self):
        self.driver.get('https://www.crowdgrader.org') #load crowdgrade
        time.sleep(demo_time) #sleep for 2 seconds for demoing purpose, otherwise it is too fast
        login = self.driver.find_element_by_css_selector('.btn-login').click() # find in the log in button by css class and click on it
        current_url = self.driver.current_url # get the current url
        parsed_uri = urlparse( current_url) #parse the url
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri) #get domain from the url
        time.sleep(demo_time)
        self.assertEqual('https://accounts.google.com/', domain) #assert that the domain is google.com
        print('Login test passed: redirected to ' + domain)

    # This works the same as login
    def test_signup(self):
        self.driver.get('https://www.crowdgrader.org')
        time.sleep(demo_time)
        login = self.driver.find_element_by_css_selector('.btn-signup').click()
        current_url = self.driver.current_url
        parsed_uri = urlparse( current_url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        time.sleep(demo_time)
        self.assertEqual('https://accounts.google.com/', domain)
        print('Sign up test passed: redirected to ' + domain)

    def test_follow_link_from_home_page(self):
        self.driver.get('https://www.crowdgrader.org')
        time.sleep(demo_time)
        self.assertEqual('CrowdGrader: Peer Grading for Your Classroom', self.driver.title) #asser that the home page has title rowdGrader: Peer Grading for Your Classroom'
        print('Page title=' + self.driver.title)
        dropdown_links = self.driver.find_elements_by_class_name('dropdown-toggle') #the the dropdown menus by css class name
        dropdown_links[2].click() #click on the second dropdown menu
        time.sleep(1) #sleep for 1 second so that we make sure the dropdown menu is opened
        self.driver.find_element_by_link_text("Documentation").click() #click on the link with the text "Documention"
        time.sleep(demo_time)

        # Switch to a new window because the link will open a new window
        from selenium.webdriver.support.wait import WebDriverWait 

        # wait to make sure there are two windows open
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) == 2)

        # switch windows
        self.driver.switch_to_window(self.driver.window_handles[1])

        # wait to make sure the new window is loaded
        WebDriverWait(self.driver, 10).until(lambda d: d.title != "")
        
        # Asssert that to correct url is loaded by clicking documentation, self.drive.current_url is the current_url
        # we check if it is http://doc.crowdgrader.org/crowdgrader-documentation
        self.assertEqual('http://doc.crowdgrader.org/crowdgrader-documentation', self.driver.current_url)
        print('Current url=' + self.driver.current_url)

        # Find the Testimonial link (by its text) on the new page and lick on it
        self.driver.find_element_by_link_text('Testimonials').click()
        time.sleep(demo_time)

        #Check if correct url is loaded, as above
        self.assertEqual('http://doc.crowdgrader.org/testimonials', self.driver.current_url)
        print('Current url:' + self.driver.current_url)


        # Find a html span element by css id = #sites-page-title
        span = self.driver.find_element_by_id('sites-page-title')

        # Make sure the element has text Testimonials
        self.assertEqual('Testimonials', span.text)
        print('Main text in page:' + span.text)

        # Find the search input field by id
        search_input = self.driver.find_element_by_id('jot-ui-searchInput')

        # Write "text" to the search field
        search_input.send_keys("test")

        time.sleep(demo_time)

        # Find and click the search button
        search_button = self.driver.find_element_by_id('sites-searchbox-search-button')
        search_button.click()

        time.sleep(1)

        # Make sure search button get the correct url
        self.assertEqual('http://doc.crowdgrader.org/system/app/pages/search?scope=search-site&q=test', self.driver.current_url)
        print('Current url:' + self.driver.current_url)

        time.sleep(1)

        # Make sure search results contains a link to "Privacy Policy"
        result = self.driver.find_element_by_link_text("Privacy Policy")

        # Make sure we can click on Privacy Policy
        result.click()

    # This is called after each test
    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()