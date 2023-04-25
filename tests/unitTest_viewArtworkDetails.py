# Unit test file to determine if the Artwork Details page is displayed when the user
# clicks the a piece of artwork in the home page of Drawing Board
# application.
# This was a Sprint 2 test.

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_ll(self):

        driver = self.driver
        driver.maximize_window()

        # driver.get("http://127.0.0.1:8000")
        driver.get("http://webappgroupseven.pythonanywhere.com/")
        time.sleep(3)

        # find a piece of Artwork and click it – note this is all one Python statement
        elem = driver.find_element_by_xpath("/html/body/div[5]/section/a[1]").click()

        time.sleep(5)
        try:
            # verify Artwork Detail page exists on new screen after clicking that piece

            # attempt to find the Artwork Title
            elem = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/p[1]")
            # attempt to find the Artwork Artist
            elem = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/a[1]")
            # attempt to find 'Back to Home' Button
            elem = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/a[2]").click()
            # make sure it takes the user back to the homepage.
            elem = driver.find_element_by_xpath("/html/body/div[5]/section/a[1]")

            assert True

        except NoSuchElementException:
            self.fail("Artwork Details are not visible when clicked.")
            assert False

    time.sleep(2)


def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()
