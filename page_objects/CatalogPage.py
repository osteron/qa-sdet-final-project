from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage


class CatalogPage(BasePage):
    BREADCRUMB = (By.CLASS_NAME, 'breadcrumb')
    LIST_GROUP = (By.CLASS_NAME, 'list-group')
    LIST_GROUP_ITEMS = (By.CLASS_NAME, 'list-group-item')
    CONTENT = (By.ID, 'content')
    PRODUCT_LAYOUT = (By.CLASS_NAME, 'product-layout')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(self.driver.url + "/smartphone")

    def check_elements_on_page(self):
        assert self.check_title_page('Phones & PDAs')
        self.element(self.BREADCRUMB)
        assert len(self.elements(self.PRODUCT_LAYOUT)) == 3, f'{len(self.elements(self.PRODUCT_LAYOUT))} != 2'
        self.element(self.LIST_GROUP)
        assert len(self.elements(self.LIST_GROUP_ITEMS)) == 8, f'{len(self.elements(self.LIST_GROUP_ITEMS))} != 8'
        self.element(self.CONTENT)
