import pytest

from site_autotest.pages.main_page import *
from site_autotest.utils import unique_number
import random

class TestSupport(object):
    @pytest.fixture(autouse=True)
    def setup_method(self, driver_fixture, variables):
        self.driver = driver_fixture
        self.main_page = MainPage(self.driver, variables)
        self.main_page.open()
        random.seed()

    def generate_subject_for_anonymous_user(self):
        return "automation_test_ticket:user - anonymous %s" % str(unique_number())

    def generate_subject_for_registered_user(self, username):
        return "automation_test_ticket:user - %s" % username

    def generate_message_for_user(self, email):
        return "test  - email:%s" % email

    def test_send_message_to_support_by_anonymous_user(self):
        email = QA_EMAIL
        subject = self.generate_subject_for_anonymous_user()
        message = self.generate_message_for_user(email)
        contact_page = self.main_page.open_contact_page()
        message_sent_page = contact_page.send_message_to_support(email, subject, message)
        self.assert_that_message_sending_is_successful(message_sent_page)

    def test_send_message_to_support_by_registered_user(self):
        client_area_page, user = self.main_page.login_random_exist_user('send_message_to_support')
        client_area_page.go_to_main_page()
        email = user.email
        subject = self.generate_subject_for_registered_user(user.username)
        message = self.generate_message_for_user(email)
        contact_page = self.main_page.open_contact_page()
        message_sent_page = contact_page.send_message_to_support(email, subject, message)
        self.assert_that_message_sending_is_successful(message_sent_page)

    def assert_that_message_sending_is_successful(self, message_sent_page):
        assert message_sent_page.exist_success_message()
