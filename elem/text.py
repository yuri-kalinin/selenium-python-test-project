from selenium.webdriver.common.by import By
from .elembase import ElemBase

class Text(ElemBase):
    def __init__(self, page, model: str):
        super().__init__(page, (By.CSS_SELECTOR, f'[ng-model="{model}"]'))

    def set_value(self, value):
        self.find().clear()
        self.find().send_keys(value)

    def get_value(self):
        return self.find().get_attribute("value")