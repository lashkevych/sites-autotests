import time

from site_autotest.settings import SITE_URL, DELAY_BETWEEN_ATTEMPTS


class MainPage(object):
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(SITE_URL)

    def go_to_payment_page(self):
        self.driver.find_element_by_link_text('ORDER').click()


class LoginForm(object):
    def __init__(self, driver):
        self.driver = driver
        self.main_page = MainPage(driver)

    def open(self):
        self.main_page.open()
        self.driver.find_element_by_id("login").click()
        time.sleep(DELAY_BETWEEN_ATTEMPTS)

    def login(self, username_or_email, password):
        self.open()
        self.enter_username_or_email(username_or_email)
        self.enter_password(password)
        self.press_login_button()

    def enter_password(self, password):
        password_element = self.driver.find_element_by_id("login-password")
        password_element.click()
        password_element.clear()
        password_element.send_keys(password)

    def enter_username_or_email(self, username_or_email):
        username_or_email_element = self.driver.find_element_by_id("username_or_email")
        username_or_email_element.click()
        username_or_email_element.clear()
        username_or_email_element.send_keys(username_or_email)

    def press_login_button(self):
        self.driver.find_element_by_xpath(
            "//form[@action='/en/login']/input[@type='submit']").click()