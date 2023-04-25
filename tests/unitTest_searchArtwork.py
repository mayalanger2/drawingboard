# Unit test file to determine if a successful search brings up Artwork and that the
# piece of Artwork shows its title and artist.  Details for both are checked to make sure
# they exist.
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

        # find the search bar and enter a search
        search_term = "oil"
        elem = driver.find_element_by_xpath("/html/body/div[2]/form/div/div[1]/input")
        elem.send_keys(search_term)
        # click the 'Search' button
        elem = driver.find_element_by_xpath("/html/body/div[2]/form/div/div[2]/button").click()
        time.sleep(5)

        try:
            # verify Artwork is present when searched

            # attempt to find a piece of Artwork
            elem = driver.find_element_by_xpath("/html/body/div[5]/div[3]/div[1]/a/img")
            # attempt to find a message stating '# results found for "oil":'
            elem = driver.find_element_by_xpath("/html/body/div[3]/div[1]/h2")
            # find the title of the Artwork
            elem = driver.find_element_by_xpath("/html/body/div[5]/div[3]/div[2]/h1/a")
            # find the artist for the Artwork
            elem = driver.find_element_by_xpath("/html/body/div[5]/div[3]/div[2]/p[1]/a")

            time.sleep(3)
            try:
                # attempt to get to the artwork details page from clicking the title
                elem = driver.find_element_by_xpath("/html/body/div[5]/div[3]/div[2]/h1/a").click()
                time.sleep(3)
                # attempt to get to the Artist's page from the Artwork Details.
                elem = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/a[1]/p").click()
                time.sleep(3)
                # find the Artist's name showing that we are on the Artist's details page.
                elem = driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr[1]/td/h1")
            except NoSuchElementException:
                self.fail("Artwork details not viewable.")
                assert False

            # time.sleep(3)
            try:
                # find the 'Home' button and click
                elem = driver.find_element_by_xpath("/html/body/nav/div/ul/li[1]/a").click()
                # attempt to find the "All Artwork" indicator showing that the search has reset and that we are on the
                # homepage.
                elem = driver.find_element_by_xpath("/html/body/div[5]/h4")
            except NoSuchElementException:
                self.fail("Home page did not refresh the search.")
                assert False

            assert True

        except NoSuchElementException:
            self.fail("No Artwork was found for an appropriate search term.")
            assert False

    time.sleep(2)


def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()
