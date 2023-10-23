import json
import logging
import os
import random
import time

import allure
import pytest
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver

logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger()


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="Browser to run tests", choices=["chrome", "firefox"])
    parser.addoption("--url", default="http://localhost:8081", help="Opencart URL")
    parser.addoption("--bv", default="117.0")
    parser.addoption("--executor", default="local")
    parser.addoption("--vnc", default=False)
    parser.addoption("--logs", default=False)


@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    url = request.config.getoption("--url")
    vnc = request.config.getoption("--vnc")
    version = request.config.getoption("--bv")
    logs = request.config.getoption("--logs")

    if executor == "local":
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(options=options)
        elif browser == "firefox":
            driver = webdriver.Firefox()
        else:
            raise Exception("Driver not supported")
    else:
        if browser == "chrome":
            options = ChromeOptions()
        elif browser == "firefox":
            options = FirefoxOptions()

        executor_url = f"http://{executor}:4444/wd/hub"
        caps = {
            "browserName": browser,
            "browserVersion": version,
            "selenoid:options": {
                "enableVNC": vnc,
                "enableLog": logs
            }
        }
        for k, v in caps.items():
            options.set_capability(k, v)

        driver = webdriver.Remote(
            command_executor=executor_url,
            options=options,
        )

    driver.maximize_window()
    driver.url = url
    driver.implicitly_wait(5)

    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.capabilities, indent=4),
        attachment_type=allure.attachment_type.JSON)

    request.addfinalizer(driver.close)
    return driver
