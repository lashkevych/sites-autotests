# -*- coding: utf-8 -*-
import pytest

from site_autotest.pages.main import *
from site_autotest.utils import *


class TestLogin(object):
    @pytest.fixture(autouse=True)
    def setup_method(self, selenium):
        self.driver = selenium
        self.main_page = MainPage(self.driver)
        self.main_page.open()
        self.login_form = self.main_page.get_login_form()
        self.user = create_user()

    def test_login_using_username(self):
        self.login_form.login(self.user.username, self.user.password)
        self.assert_that_logout_link_exist()

    def test_login_using_email(self):
        self.login_form.login(self.user.email, self.user.password)
        self.assert_that_logout_link_exist()

    def assert_that_logout_link_exist(self):
        if TEST_RESELLER == 'anonine':
            self.driver.find_element_by_xpath("//a[@href='/en/logout']")
        elif TEST_RESELLER == 'box-pn':
            self.driver.find_element_by_xpath("//a[@href='/logout']")
        else:
            pytest.fail('unknown reseller in assert login test')
#    pytest.fail('Account.text is empty ')
