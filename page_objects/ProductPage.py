from selenium.webdriver.common.by import By

from page_objects.BasePage import BasePage


class ProductPage(BasePage):
    IMAGES = (By.CSS_SELECTOR, '#content .row .thumbnail')
    ADD_TO_WISHLIST = (By.XPATH, '//div[@class="btn-group"]/button[@data-original-title="Add to Wish List"]')
    COMPARE_THIS_PRODUCT = (By.XPATH, '//div[@class="btn-group"]/button[@data-original-title="Compare this Product"]')
    PRODUCT_NAME = (By.CSS_SELECTOR, '.col-sm-4 h1')
    ADD_TO_CARD = (By.CSS_SELECTOR, '#product .form-group button')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(self.driver.url + "/iphone")

    def check_elements_on_page_of_iphone(self):
        assert self.check_title_page('iPhone')
        assert len(self.elements(self.IMAGES)) == 6
        self.element(self.ADD_TO_WISHLIST)
        self.element(self.COMPARE_THIS_PRODUCT)
        self.element(self.ADD_TO_CARD)
        assert self.get_text_of_element(self.PRODUCT_NAME).lower() in 'iphone'
