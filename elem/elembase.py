from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

class ElemBase(object):

    def __init__(self, page, locator: (By, str)):   
        self.driver: WebDriver = page.driver
        self.wait: WebDriverWait = page.wait
        self.locator: (By, str) = locator

    def find(self):
        return self.driver.find_element(*self.locator)
    
    def find_all(self):
        return self.driver.find_elements(*self.locator)

    def click(self):
        self.find().click()

    def is_displayed(self):
        try:
            return self.find().is_displayed()
        except Exception:
            return False

    def wait_until_displayed(self, visible: bool=True):
        if visible:
            self.wait.until(expected_conditions.visibility_of_element_located(self.locator))
        else:
            self.wait.until(expected_conditions.invisibility_of_element_located(self.locator))