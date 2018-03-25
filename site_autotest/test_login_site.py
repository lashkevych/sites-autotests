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

    def test_login(self):
        user = create_user()
        self.go_to_login_page()
        self.enter_username(user.username)
        self.enter_password(user.password)
        self.press_login_button()
        self.assert_that_username_on_account_dashboard_is_equal_to(user.username)
        # TODO user should have active status
        #def username_on_account_dashboard():
        #    return ...
        #assert_that(username_on_account_dashboard(), equal_to(username))
        #assert_that_eventually(username_on_account_dashboard, equal_to(username))

    def assert_that_username_on_account_dashboard_is_equal_to(self, username):
        account = self.driver.find_element_by_class_name('account')
        count_max = int(WAIT_TIMEOUT / DELAY_BETWEEN_ATTEMPTS)
        for _ in range(count_max):
            if account.text != '':
                assert 'Username: %s' % username in account.text
                break
            else:
                time.sleep(DELAY_BETWEEN_ATTEMPTS)
        else:
            #self.fail('Account.text is empty ')
            pytest.fail('Account.text is empty ')

    def go_to_main_page(self):
        self.driver.get(SITE_URL)

    def go_to_login_page(self):
        self.go_to_main_page()
        self.driver.find_element_by_id("loginLink").click()

    def enter_password(self, password):
        password_element = self.driver.find_element_by_id("password")
        password_element.click()
        password_element.clear()
        password_element.send_keys(password)

    def enter_username(self, username):
        username_element = self.driver.find_element_by_id("username_or_email")
        username_element.click()
        username_element.clear()
        username_element.send_keys(username)

    def press_login_button(self):
        self.driver.find_element_by_xpath("//button[@type='submit']").click()

    def teardown_method(self, method):
        #TODO: add pytest selenium plugin for making screenshots and other usefull things
        #if self.failureException is not None:
         #   self.driver.save_screenshot("Screenshots\%s.png" % method)
        self.driver.quit()
