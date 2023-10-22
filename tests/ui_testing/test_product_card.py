import allure

from page_objects.ProductPage import ProductPage


@allure.feature("Product card content")
@allure.title("Check product card content of iphone")
def test_product_card_content(browser):
    ProductPage(browser).check_elements_on_page_of_iphone()
