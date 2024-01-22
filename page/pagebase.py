from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import elem

class PageBase:

    def __init__(self, page):
        self.url: str = page.url
        self.driver: WebDriver = page.driver
        self.wait: WebDriverWait = page.wait

        self.logout = elem.Button(page, click="logout()")
        self.alerts = elem.Link(page, sref="app.alert")

    def wait_loading_complete(self, timeout: float=2):
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "preloader.ng-scope")))
        except TimeoutException:
            pass
        finally:
            self.wait.until(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "preloader.ng-scope.ng-hide")))

    def wait_errors(self, timeout: float=3) -> list[str]:
        errors = []
        try:
            wait = WebDriverWait(self.driver, timeout)
            messages = wait.until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "message.ng-binding")))
            errors.extend(message.text for message in messages)
        except Exception:
            pass
        finally:
            return errors

    def open(self):
        self.driver.get(self.url)
        self.wait_loading_complete()
        
    def is_opened(self):
        return self.driver.current_url == self.url