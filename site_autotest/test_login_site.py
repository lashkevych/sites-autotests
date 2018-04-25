# -*- coding: utf-8 -*-

import pytest

from selenium import webdriver

from site_autotest.utils import *
from .settings import *


class TestLogin(object):
    def setup_method(self):
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(WAIT_TIMEOUT)

    def test_login_using_username(self):
        user = create_user()
        self.open_login_form()
        self.enter_username_or_email(user.username)
        self.enter_password(user.password)
        self.press_login_button()
        self.assert_that_logout_link_exist()
        # TODO user should have active status

    def test_login_using_email(self):
        user = create_user()
        self.open_login_form()
        self.enter_username_or_email(user.email)
        self.enter_password(user.password)
        self.press_login_button()
        self.assert_that_logout_link_exist()

    def assert_that_logout_link_exist(self):
        self.driver.find_element_by_xpath("//a[@href='/en/logout']")

    def go_to_main_page(self):
        self.driver.get(SITE_URL)

    def open_login_form(self):
        self.go_to_main_page()
        self.driver.find_element_by_id("login").click()
        time.sleep(DELAY_BETWEEN_ATTEMPTS)

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


    def teardown_method(self, method):
        #TODO: add pytest selenium plugin for making screenshots and other usefull things
        #if self.failureException is not None:
         #   self.driver.save_screenshot("Screenshots\%s.png" % method)
        self.driver.quit()


#    pytest.fail('Account.text is empty ')
