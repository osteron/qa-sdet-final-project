import logging
import os.path
import allure
from selenium.webdriver import ActionChains
from typing import AnyStr, List
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

logger = logging.getLogger(__name__)


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def save_screenshot(self):
        index = 0
        os.makedirs("screenshots", exist_ok=True)
        while os.path.exists(f"screenshots/{index}.png"):
            index += 1
        self.driver.get_screenshot_as_file(f"screenshots/{index}.png")

    @allure.step('Input text to {element}')
    def _input(self, element, value) -> None:
        self.click(element)
        element.clear()
        element.send_keys(value)

    @allure.step('Waiting element {locator}')
    def element(self, locator: tuple) -> WebElement:
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(locator))
        except TimeoutException as e:
            logger.exception(e)
            allure.attach(
                name="Screenshot",
                body=self.driver.get_screenshot_as_png(),
                attachment_type=allure.attachment_type.PNG
            )
            self.save_screenshot()
            raise AssertionError(f'Не дождался видимости элемента {locator}')

    @allure.step('Waiting not visible element {locator}')
    def not_visible_element(self, locator: tuple) -> bool:
        try:
            return WebDriverWait(self.driver, 2).until(EC.invisibility_of_element_located(locator))
        except TimeoutException as e:
            logger.exception(e)
            allure.attach(
                name="Screenshot",
                body=self.driver.get_screenshot_as_png(),
                attachment_type=allure.attachment_type.PNG
            )
            self.save_screenshot()
            raise AssertionError(f'Элемент до сих пор виден {locator}')

    @allure.step('Click button')
    def click(self, element) -> None:
        ActionChains(self.driver).move_to_element(element).pause(0.1).click().perform()

    @allure.step('Waiting elements {locator}')
    def elements(self, locator: tuple) -> List[WebElement]:
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located(locator))
        except TimeoutException as e:
            logger.exception(e)
            allure.attach(
                name="Screenshot",
                body=self.driver.get_screenshot_as_png(),
                attachment_type=allure.attachment_type.PNG
            )
            self.save_screenshot()
            raise AssertionError(f'Не дождался видимости элементов {locator}')

    @allure.step('Get text of element {locator}')
    def get_text_of_element(self, locator: tuple) -> AnyStr:
        return self.element(locator).text

    @allure.step('Check title with {title}')
    def check_title_page(self, title: str) -> bool:
        return self.driver.title in title

    @allure.step('Accept alert')
    def alert_accept(self) -> None:
        try:
            Alert(self.driver).accept()
        except:
            return
