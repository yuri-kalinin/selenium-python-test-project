from selenium.webdriver.common.by import By
from .elembase import ElemBase

class Table(ElemBase):
    def __init__(self, page, repeat: str):
        super().__init__(page, (By.CSS_SELECTOR, f'[ng-repeat="{repeat}"]'))
    
    def get_data(self) -> list[list[str]]:
        data = []
        try:
            for row in self.find_all():
                data.append([td.text for td in row.find_elements(By.TAG_NAME, 'td')])
        except Exception:
            #This is a workaround for the case where the rows get stale
            data.clear()
            for row in self.find_all():
                data.append([td.text for td in row.find_elements(By.TAG_NAME, 'td')])
        finally:
            return data