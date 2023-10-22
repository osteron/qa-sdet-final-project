import allure
from page_objects.CatalogPage import CatalogPage


@allure.feature("Check page content")
@allure.title("Check smartphone page content")
def test_catalog_page_content(browser):
    CatalogPage(browser).check_elements_on_page()
