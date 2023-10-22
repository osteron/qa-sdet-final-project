import allure
from page_objects.RegisterPage import RegisterPage


@allure.feature("Registration")
@allure.title("Registration new user")
def test_register_user(browser):
    RegisterPage(browser).register_new_user()
