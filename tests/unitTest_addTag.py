import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


# Unit test file to determine if a tag can be
# successfully created in the Admin side of DrawingBoard.
# This was a S1 test.

class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_ll(self):
        user = "groupseven"
        pwd = "Groupseven123!"

        driver = self.driver
        driver.maximize_window()
        # driver.get("http://127.0.0.1:8000/admin")
        driver.get("http://webappgroupseven.pythonanywhere.com/admin")
        elem = driver.find_element_by_id("id_username")
        elem.send_keys(user)
        elem = driver.find_element_by_id("id_password")
        elem.send_keys(pwd)
        time.sleep(3)
        elem.send_keys(Keys.RETURN)

        # after login, go to the Tags page.
        # driver.get("http://127.0.0.1:8000/admin/gallery/tag/")
        driver.get("http://webappgroupseven.pythonanywhere.com/admin/gallery/tag")
        time.sleep(3)
        # find the 'ADD TAG' button and click
        elem = driver.find_element_by_xpath("/html/body/div/div[3]/div/div[1]/div/ul/li/a").click()

        tag_name = "portraits"
        tag_description = "Portraits are pictures of different people."
        time.sleep(3)
        elem = driver.find_element_by_id("id_tag_name")
        elem.send_keys(tag_name)
        time.sleep(3)
        elem = driver.find_element_by_id("id_tag_description")
        elem.send_keys(tag_description)
        time.sleep(3)

        # Find save button and click.
        elem = driver.find_element_by_xpath("/html/body/div/div[3]/div/div[1]/div/form/div/div/input[1]").click()

        try:
            # find the success indicator
            elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/ul/li")

            # find that there is a field in the Tags
            elem = driver.find_element_by_xpath(
                "/html/body/div/div[3]/div/div[1]/div/div/div/form/div[2]/table/tbody/tr[1]/th/a")
            assert True

        except NoSuchElementException:
            self.fail("Tag was not created.")
            assert False

        time.sleep(3)


def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()
