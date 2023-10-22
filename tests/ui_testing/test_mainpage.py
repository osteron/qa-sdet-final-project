import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from page_objects.MainPage import MainPage


@allure.feature("Main page content")
@allure.title("Check main page content")
def test_main_page_content(browser: WebDriver) -> None:
    MainPage(browser).check_elements_on_page()


@allure.feature("Main page content")
@allure.title("Check switching of all currencies")
def test_switching_currencies(browser: WebDriver) -> None:
    MainPage(browser).switching_all_currencies()
