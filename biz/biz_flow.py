from pages.login_page import LoginPage
from pages.home_page import HomePage


class BizFlow:
    def __init__(self, driver):
        self.login_page = LoginPage(driver)
        self.home_page = HomePage(driver)

    def login_and_verify(self, email, password):
        self.login_page.login(email, password)
        return self.home_page.is_logged_in()
