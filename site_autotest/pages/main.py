import time

from site_autotest.settings import SITE_URL, DELAY_BETWEEN_ATTEMPTS
from site_autotest.pages.control_panel import ControlPanelPage
from site_autotest.pages.payment import PaymentPage

class MainPage(object):
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(SITE_URL)

    def open_payment_page(self):
        self.driver.find_element_by_link_text('ORDER').click()
        return PaymentPage(self.driver)

    def open_login_form(self):
        #self.driver.find_element_by_id("login").click()
        time.sleep(DELAY_BETWEEN_ATTEMPTS)
        return LoginForm(self.driver)

class LoginForm(object):
    def __init__(self, driver):
        self.driver = driver

    def login(self, username_or_email, password):
        self.enter_username_or_email(username_or_email)
        self.enter_password(password)
        return self.submit_login()

    def enter_password(self, password):
        #password_element = self.driver.find_element_by_id("login-password")
        password_element = self.driver.find_element_by_css_selector("input[name='password']")
        password_element.click()
        password_element.clear()
        password_element.send_keys(password)

    def enter_username_or_email(self, username_or_email):
        #username_or_email_element = self.driver.find_element_by_id("username_or_email")
        username_or_email_element = self.driver.find_element_by_css_selector("input[name='username_or_email']")
        username_or_email_element.click()
        username_or_email_element.clear()
        username_or_email_element.send_keys(username_or_email)

    def submit_login(self):
        #self.driver.find_element_by_xpath("//form[@action='/en/login']/input[@type='submit']").click()
        self.driver.find_element_by_xpath("//form[@id='loginForm']//button[@type='submit']").click()
        return ControlPanelPage(self.driver)