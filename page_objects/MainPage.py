from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage


class MainPage(BasePage):
    LOGO = (By.CSS_SELECTOR, '#logo')
    SEARCH = (By.ID, 'search')
    CART = (By.ID, 'cart')
    MENU = (By.ID, 'menu')
    FOOTER = (By.TAG_NAME, 'footer')
    SLIDESHOW = (By.CLASS_NAME, 'slideshow')
    PRODUCT_LAYOUT = (By.CLASS_NAME, 'product-layout')
    CURRENCY = (By.XPATH, '//*[@id="form-currency"]/div')
    CURRENT_CURRENCY = (By.CSS_SELECTOR, 'strong')
    EURO = (By.NAME, 'EUR')
    POUND_STERLING = (By.NAME, 'GBP')
    DOLLAR = (By.NAME, 'USD')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(self.driver.url)

    def check_elements_on_page(self):
        assert self.check_title_page('Your Store')
        self.element(self.LOGO)
        self.element(self.SEARCH)
        self.element(self.CART)
        self.element(self.MENU)
        self.element(self.SLIDESHOW)
        assert len(self.elements(self.PRODUCT_LAYOUT)) == 4
        self.element(self.FOOTER)

    def switching_all_currencies(self):
        assert self.get_text_of_element(self.CURRENT_CURRENCY) in '$'
        self.click(self.element(self.CURRENCY))
        self.click(self.element(self.EURO))
        assert self.get_text_of_element(self.CURRENT_CURRENCY) in '€'
        self.click(self.element(self.CURRENCY))
        self.click(self.element(self.POUND_STERLING))
        assert self.get_text_of_element(self.CURRENT_CURRENCY) in '£'
        self.click(self.element(self.CURRENCY))
        self.click(self.element(self.DOLLAR))
        assert self.get_text_of_element(self.CURRENT_CURRENCY) in '$'
