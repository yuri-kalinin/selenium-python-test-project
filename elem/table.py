from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from .elembase import ElemBase

class Table(ElemBase):
    def __init__(self, page, repeat: str):
        super().__init__(page, (By.CSS_SELECTOR, f'[ng-repeat="{repeat}"]'))
    
    def get_data(self) -> list[list[str]]:
        data = []
        try:
            for row in self.find_all():
                data.append([td.text for td in row.find_elements(By.TAG_NAME, 'td')])
        except StaleElementReferenceException:
            #This is a workaround for the case where the rows get stale
            data.clear()
            for row in self.find_all():
                data.append([td.text for td in row.find_elements(By.TAG_NAME, 'td')])
        finally:
            return data
        
    def wait_until_contains(self, value: str):
        try:
            self.wait.until(expected_conditions.text_to_be_present_in_element(self.locator, value))
        except TimeoutException:
            pass