import pytest


from site_autotest.pages.main import *
from site_autotest.utils import *

class TestResetPassword(object):
    @pytest.fixture(autouse=True)
    def setup_method(self, driver_fixture, variables):
        self.driver = driver_fixture
        self.main_page = MainPage(self.driver, variables)
        self.main_page.open()
        self.login_form = self.main_page.get_login_form()
        self.user = create_user()

    def test_reset_password_by_username(self):
        self.login_form.open_login_form()
        reset_password_form = self.login_form.open_reset_form()
        reset_password_form.send_reset_link(self.user.username)
        self.assert_that_reset_link_is_sent(reset_password_form)
        reset_password_form.go_to_login_form()

        time.sleep(DELAY_BEFORE_GETTING_EMAILS)
        new_password_form = self.main_page.get_new_password_form()
        new_password_form.open(self.user.email)
        new_password_form.enter_and_confirm_new_password()

        self.assert_that_reset_password_is_correct()

    def assert_that_reset_link_is_sent(self,reset_password_form):
        return reset_password_form.reset_link_is_sent_successfully()

    def assert_that_reset_password_is_correct(self):
        self.login_form.login(self.user.email, NEW_PASSWORD_FOR_RESET_PASSSWORD)
        assert self.main_page.exist_logout_link()
