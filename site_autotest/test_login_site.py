# -*- coding: utf-8 -*-

from selenium import webdriver

from site_autotest.pages.main import LoginForm
from site_autotest.utils import *
from .settings import *


class TestLogin(object):
    def setup_method(self):
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(WAIT_TIMEOUT)
        self.login_form = LoginForm(self.driver)
        self.user = create_user()

    def test_login_using_username(self):
        self.login_form.login(self.user.username, self.user.password)
        self.assert_that_logout_link_exist()
        # TODO user should have active status

    def test_login_using_email(self):
        self.login_form.login(self.user.email, self.user.password)
        self.assert_that_logout_link_exist()

    def assert_that_logout_link_exist(self):
        self.driver.find_element_by_xpath("//a[@href='/en/logout']")

    def teardown_method(self, method):
        #TODO: add pytest selenium plugin for making screenshots and other usefull things
        #if self.failureException is not None:
         #   self.driver.save_screenshot("Screenshots\%s.png" % method)
        self.driver.quit()


#    pytest.fail('Account.text is empty ')
