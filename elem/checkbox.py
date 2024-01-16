from selenium.webdriver.common.by import By
from .elembase import ElemBase

class Checkbox(ElemBase):
    def __init__(self, page, model: str):
        super().__init__(page, (By.CSS_SELECTOR, f'[ng-model="{model}"]'))

    def set_value(self, value: bool):
        if self.find().is_selected != value:
            self.find().find_element(By.XPATH, "..").click()

    def get_value(self):
        return self.find().is_selected()