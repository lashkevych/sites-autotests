import pytest


from site_autotest.pages.main_page import *
from site_autotest.utils import *

class TestResetPassword(object):
    @pytest.fixture(autouse=True)
    def setup_method(self, driver_fixture, variables):
        self.driver = driver_fixture
        self.main_page = MainPage(self.driver, variables)
        self.main_page.open()
        self.login_form = self.main_page.open_login_page()

    def test_reset_password_by_username(self):
        self.user = create_user('reset_password_by_username')
        reset_password_form = self.login_form.open_reset_password_page()
        reset_password_form.send_reset_link(self.user.username)
        self.assert_that_reset_link_is_sent(reset_password_form)
        reset_password_form.go_to_login_page()

        time.sleep(DELAY_BEFORE_GETTING_EMAILS)
        #TBD  - need optimization of email count
        new_password_form = self.main_page.get_new_password_page()
        new_password_form.open(self.user.email)
        new_password_form.enter_and_confirm_new_password()

        self.assert_that_reset_password_is_correct()

    def test_can_not_reset_password_by_incorrect_email(self):
        reset_password_form = self.login_form.open_reset_password_page()
        not_registered_username = generate_username()
        reset_password_form.send_reset_link(not_registered_username)

        self.assert_that_email_or_username_error_exist(reset_password_form)

    def test_change_password(self):
        self.user = create_user('change_password_in_client_area')
        client_area_page = self.login_form.login(self.user.username, self.user.password)
        profile_page = client_area_page.open_profile_page()

        profile_page.go_to_change_email_password_tab()
        profile_page.change_password(NEW_PASSWORD_FOR_RESET_PASSSWORD)
        client_area_page.logout()
        self.login_form = self.main_page.open_login_page()

        self.assert_that_reset_password_is_correct()

    def assert_that_reset_link_is_sent(self,reset_password_form):
        return reset_password_form.reset_link_is_sent_successfully()

    def assert_that_reset_password_is_correct(self):
        client_area_page = self.login_form.login(self.user.email, NEW_PASSWORD_FOR_RESET_PASSSWORD)
        assert client_area_page.exist_logout_link()

    def assert_that_email_or_username_error_exist(self, reset_password_form):
        assert reset_password_form.incorrect_email_or_username()
