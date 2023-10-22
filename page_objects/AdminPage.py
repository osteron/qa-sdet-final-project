import logging

import allure
from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage

logger = logging.getLogger(__name__)


class AdminPage(BasePage):
    HEADER_LOGO = (By.ID, 'header-logo')
    CENTER_PANEL = (By.CLASS_NAME, 'panel-default')
    PANEL_TITLE = (By.XPATH, '//h1[@class="panel-title"]/i')
    USERNAME_LABEL = (By.XPATH, '//label[@for="input-username"]')
    USERNAME_INPUT = (By.ID, 'input-username')
    PASSWORD_LABEL = (By.XPATH, '//label[@for="input-password"]')
    PASSWORD_INPUT = (By.ID, 'input-password')
    FORGOTTEN_PASSWORD = (By.CLASS_NAME, 'help-block')
    SUBMIT = (By.CSS_SELECTOR, '.btn.btn-primary i')
    USER = 'user'
    PASSWORD = 'bitnami'
    PANEL_TITLE_TEXT = 'Please enter your login details.'
    USERNAME_LABEL_TEXT = 'Username'
    PASSWORD_LABEL_TEXT = 'Password'
    SUBMIT_TEXT = 'Login'
    CATALOG = (By.ID, 'menu-catalog')
    PRODUCTS = (By.XPATH, '//*[@id="collapse1"]/li[2]')
    ADD_NEW_PRODUCT_BUTTON = (By.CSS_SELECTOR, 'a[data-original-title="Add New"]')
    PRODUCT_NAME_INPUT = (By.ID, 'input-name1')
    META_TAG_INPUT = (By.ID, 'input-meta-title1')
    SAVE_NEW_PRODUCT = (By.CLASS_NAME, 'fa-save')
    DATA_TAB = (By.LINK_TEXT, 'Data')
    MODEL_INPUT = (By.ID, 'input-model')
    CHECKBOX_NEW_PRODUCT = (By.XPATH, '//td[contains(text(), "test")][2]/../td/input')
    DELETE_PRODUCT_BUTTON = (By.CLASS_NAME, 'btn-danger')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(self.driver.url + "/admin/")

    def check_elements_on_page(self):
        assert self.check_title_page('Administration')
        self.element(self.HEADER_LOGO)
        self.element(self.CENTER_PANEL)
        self.element(self.USERNAME_INPUT)
        self.element(self.PASSWORD_INPUT)
        self.element(self.FORGOTTEN_PASSWORD)
        assert self.get_text_of_element(self.PANEL_TITLE) in self.PANEL_TITLE_TEXT
        assert self.get_text_of_element(self.USERNAME_LABEL) in self.USERNAME_LABEL_TEXT
        assert self.get_text_of_element(self.PASSWORD_LABEL) in self.PASSWORD_LABEL_TEXT
        assert self.get_text_of_element(self.SUBMIT) in self.SUBMIT_TEXT

    def admin_login(self) -> None:
        with allure.step('Login with admin credentials'):
            self._input(self.element(self.USERNAME_INPUT), self.USER)
            self._input(self.element(self.PASSWORD_INPUT), self.PASSWORD)
            try:
                self.click(self.element(self.SUBMIT))
            except Exception as e:
                logger.error("Got exception")
                logger.exception(e)
                allure.attach(
                    name="Screenshot",
                    body=self.driver.get_screenshot_as_png(),
                    attachment_type=allure.attachment_type.PNG
                )
                self.save_screenshot()
                raise e

    def go_to_products(self) -> None:
        self.click(self.element(self.CATALOG))
        self.click(self.element(self.PRODUCTS))

    def add_new_product(self, product_name: str, meta_tag: str, model_name: str) -> None:
        self.admin_login()
        self.go_to_products()
        self.click(self.element(self.ADD_NEW_PRODUCT_BUTTON))
        self._input(self.element(self.PRODUCT_NAME_INPUT), product_name)
        self._input(self.element(self.META_TAG_INPUT), meta_tag)
        self.click(self.element(self.DATA_TAB))
        self._input(self.element(self.MODEL_INPUT), model_name)
        self.click(self.element(self.SAVE_NEW_PRODUCT))
        self.element((By.XPATH, f'//td[contains(text(), "{product_name}")][1]'))
        self.element((By.XPATH, f'//td[contains(text(), "{meta_tag}")][2]'))

    def delete_product(self, product_name: str) -> None:
        self.admin_login()
        self.go_to_products()
        self.element((By.XPATH, f'//td[contains(text(), "{product_name}")][1]'))
        self.click(self.element((By.XPATH, f'//td[contains(text(), "{product_name}")][1]/../td/input')))
        self.click(self.element(self.DELETE_PRODUCT_BUTTON))
        self.alert_accept()
        self.not_visible_element((By.XPATH, f'//td[contains(text(), "{product_name}")][1]'))
