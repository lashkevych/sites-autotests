import time

import pytest

from site_autotest.config import TEST_RESELLER
from site_autotest.settings import SITE_URL, DELAY_BETWEEN_ATTEMPTS
from site_autotest.pages.control_panel import ControlPanelPage
from site_autotest.pages.payment import PaymentPage


class MainPage(object):
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(SITE_URL)

    def open_payment_page(self):
        if TEST_RESELLER == 'anonine':
            self.driver.find_element_by_link_text('BUY').click()
        elif TEST_RESELLER == 'box-pn':
            self.driver.find_element_by_link_text('Order').click()
        else:
            pytest.fail('unknown reseller in open order page')
        return PaymentPage(self.driver)

    def open_client_area_page(self):
        if TEST_RESELLER == 'anonine':
            self.driver.find_element_by_link_text('ACCOUNT').click()
        elif TEST_RESELLER == 'box-pn':
            self.driver.find_element_by_link_text('CLIENT AREA').click()
        else:
            pytest.fail('unknown reseller in open order page')
        return ControlPanelPage(self.driver)

    def get_login_form(self):
        return LOGIN_FORMS[TEST_RESELLER](self.driver)


class AnonineLoginForm(object):
    def __init__(self, driver):
        self.driver = driver

    def login(self, username_or_email, password):
        self.open_login_form()
        self.enter_username_or_email(username_or_email)
        self.enter_password(password)
        return self.submit_login()

    def open_login_form(self):
        self.driver.find_element_by_id("loginLink").click()
        time.sleep(DELAY_BETWEEN_ATTEMPTS)

    def enter_username_or_email(self, username_or_email):
        username_or_email_element = self.driver.find_element_by_id("username_or_email")
        username_or_email_element.click()
        username_or_email_element.clear()
        username_or_email_element.send_keys(username_or_email)

    def enter_password(self, password):
        password_element = self.driver.find_element_by_id("password")
        password_element.click()
        password_element.clear()
        password_element.send_keys(password)

    def submit_login(self):
        self.driver.find_element_by_xpath("//form[@class='login_form']//button[@type='submit']").click()
        return ControlPanelPage(self.driver)


class BoxpnLoginForm(object):
    def __init__(self, driver):
        self.driver = driver

    def login(self, username_or_email, password):
        self.enter_username_or_email(username_or_email)
        self.enter_password(password)
        return self.submit_login()

    def enter_username_or_email(self, username_or_email):
        username_or_email_element = self.driver.find_element_by_css_selector("input[name='username_or_email']")
        username_or_email_element.click()
        username_or_email_element.clear()
        username_or_email_element.send_keys(username_or_email)

    def enter_password(self, password):
        password_element = self.driver.find_element_by_css_selector("input[name='password']")
        password_element.click()
        password_element.clear()
        password_element.send_keys(password)


    def submit_login(self):
        self.driver.find_element_by_xpath("//form[@id='loginForm']//button[@type='submit']").click()
        return ControlPanelPage(self.driver)


LOGIN_FORMS = {
    'anonine': AnonineLoginForm,
    'box-pn': BoxpnLoginForm,
}