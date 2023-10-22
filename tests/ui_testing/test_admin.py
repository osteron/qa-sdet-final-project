import allure
from page_objects.AdminPage import AdminPage


@allure.feature("Admin page")
class TestAdminPage:

    @allure.title("Check admin page content")
    def test_admin_page_content(self, browser):
        AdminPage(browser).check_elements_on_page()

    @allure.title("Admin add new product")
    def test_add_new_product(self, browser):
        AdminPage(browser).add_new_product('test', 'test', 'test')

    @allure.title("Admin delete product")
    def test_delete_product(self, browser):
        AdminPage(browser).delete_product('test')
