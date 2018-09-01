# -*- coding: utf-8 -*-
import pytest

from site_autotest.pages.main import *
from site_autotest.utils import *


class TestLogin(object):
    @pytest.fixture(autouse=True)
    def setup_method(self, driver_fixture, variables):
        self.driver = driver_fixture
        #self.driver.set_window_size(300, 500)
        self.main_page = MainPage(self.driver, variables)
        self.main_page.open()
        self.login_form = self.main_page.get_login_form()
        self.user = create_user()

    def test_login_using_username(self):
        self.login_form.open_login_form()
        self.login_form.login(self.user.username, self.user.password)
        self.assert_that_logout_link_exist()

    def test_login_using_email(self):
        self.login_form.open_login_form()
        self.login_form.login(self.user.email, self.user.password)
        self.assert_that_logout_link_exist()

    def assert_that_logout_link_exist(self):
        assert self.main_page.exist_logout_link()
