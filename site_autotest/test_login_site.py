# -*- coding: utf-8 -*-
import pytest

from site_autotest.pages.main_page import *
from site_autotest.utils import *


class TestLogin(object):
    @pytest.fixture(autouse=True)
    def setup_method(self, driver_fixture, variables):
        self.driver = driver_fixture
        self.main_page = MainPage(self.driver, variables)
        self.main_page.open()
        self.login_form = self.main_page.open_login_page()
        self.user = create_user()

    def test_login_using_username(self):
        client_area_page = self.login_form.login(self.user.username, self.user.password)
        self.assert_that_login_is_successful(client_area_page)

    def test_login_using_email(self):
        client_area_page = self.login_form.login(self.user.email, self.user.password)
        self.assert_that_login_is_successful(client_area_page)

    def test_can_not_login_using_correct_username_and_incorrect_password(self):
        self.login_form.can_not_login(self.user.username, self.user.password+'1')
        self.assert_that_password_error_exist()

    def assert_that_login_is_successful(self, client_area_page):
        assert client_area_page.exist_logout_link()

    def assert_that_password_error_exist(self):
        assert self.login_form.exist_password_error()

