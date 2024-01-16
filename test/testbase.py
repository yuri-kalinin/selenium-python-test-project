import os
import warnings
from pathlib import Path

import pytest
import yaml

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

#Turn off webdriver-manager logs use
os.environ['WDM_LOG_LEVEL'] = '0'


def get_config():
    path = Path(__file__).parent / "../config.yaml"
    with open(path) as config_file:
        data = yaml.load(config_file, Loader=yaml.FullLoader)
    return data


class TestBase:

    @pytest.fixture(scope="session", autouse=True)
    def init_test(self):
        self.config = get_config()
        warnings.simplefilter("ignore", ResourceWarning)
        if self.config['browser'] == 'chrome':
            options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(options=options)
        elif self.config['browser'] == 'firefox':
            options = webdriver.FirefoxOptions()
            self.driver = webdriver.Firefox(options=options)
        else:
            raise Exception("Incorrect Browser")

        options.add_argument('--log-level=3')

        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = self.config['url']
        yield self.wait, self.driver

        if self.driver is not None:
            self.driver.close()
            self.driver.quit()
