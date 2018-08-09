import pytest

from Utils.emailR import EmailServerWrapper
from site_autotest.pages.main import *
from site_autotest.utils import *

class TestResetPassword(object):
    @pytest.fixture(autouse=True)
    def setup_method(self, driver_fixture):
        self.driver = driver_fixture
        self.main_page = MainPage(self.driver)
        self.main_page.open()
        self.login_form = self.main_page.get_login_form()
        self.user = create_user()

    def test_reset_password_by_username(self):
        #reset_password_form = self.login_form.open_reset_form()
        #reset_password_form.send_reset_link(self.user.username)
        #self.assert_that_reset_link_is_sent(reset_password_form)

        email_server_wrapper = EmailServerWrapper(QA_EMAIL, QA_EMAIL_PASSWORD)
        email_server_wrapper.readMail()
        #self.driver.execute_script("window.open('http://google.com', 'new_window')")
        #self.driver.switch_to_window(self.driver.window_handles[0])

        self.assert_that_reset_password_is_correct()
        #driver.execute_script("window.open('http://google.com', 'new_window')")
        #driver.switch_to_window(driver.window_handles[0])
        #driver.title

    def assert_that_reset_link_is_sent(self,reset_password_form):
        return reset_password_form.reset_link_is_sent_successfully()

    def assert_that_reset_password_is_correct(self):
        return pytest.fail('TO BE DONE')
