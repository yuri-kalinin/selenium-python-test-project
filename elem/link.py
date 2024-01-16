from selenium.webdriver.common.by import By
from .elembase import ElemBase

class Link(ElemBase):
    def __init__(self, page, sref: str):
        super().__init__(page, (By.CSS_SELECTOR, f'[ui-sref="{sref}"]'))