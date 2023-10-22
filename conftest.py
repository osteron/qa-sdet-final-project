import json
import logging

import allure
import pytest
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver

logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger()


@pytest.fixture(scope="session")
def url(request):
    return request.config.getoption("--url")


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="Browser to run tests")
    parser.addoption("--url", default="http://localhost:8081", help="Opencart URL")
    parser.addoption("--executor", default="127.0.0.1")
    parser.addoption("--drivers", default="/chromedriver", help="Drivers path")


@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")
    driver = request.config.getoption("--drivers")
    executor = request.config.getoption("--executor")
    url = request.config.getoption("--url")
    executor_url = f"http://{executor}:4444/wd/hub"
    if browser == "chrome":
        driver = webdriver.Chrome(service=ChromeService())
    elif browser == "firefox":
        driver = webdriver.Firefox(service=FirefoxService())
    else:
        raise ValueError(f'Driver {browser} not supported.')

    request.addfinalizer(driver.close)

    driver.maximize_window()
    driver.get(url)
    driver.url = url
    driver.implicitly_wait(5)

    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.capabilities, indent=4),
        attachment_type=allure.attachment_type.JSON)

    return driver
