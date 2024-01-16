from selenium.webdriver.common.by import By
from .elembase import ElemBase

class Button(ElemBase):
    def __init__(self, page, click: str):
        super().__init__(page, (By.CSS_SELECTOR, f'[ng-click="{click}"]'))