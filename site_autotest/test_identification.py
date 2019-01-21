import pytest
from site_autotest.pages.main_page import MainPage
from site_autotest.pages.payment_page import Payment
from Utils.emailR import AnonineEmailClientWrapper

from site_autotest.utils import *

def confirm_email(driver, user_email):
    email_client_wrapper = AnonineEmailClientWrapper(QA_EMAIL, QA_EMAIL_PASSWORD)
    subject = 'Thank you for your Interest in our Anonine Service!'
    link_text = 'VERIFY MY EMAIL ADDRESS'
    confirm_email_link = email_client_wrapper.get_link(user_email, subject, link_text)
    script_open_window = "window.open('%s', 'new_window')" % confirm_email_link
    driver.execute_script(script_open_window)
    driver.switch_to_window(driver.window_handles[0])

class TestIdentification(object):
    @pytest.fixture(autouse=True)
    def setup_method(self, driver_fixture, variables):
        self.driver = driver_fixture
        self.main_page = MainPage(self.driver, variables)
        self.main_page.open()

    def test_confirm_email_after_payment(self):
        payment_page = self.main_page.open_payment_page()
        user = generate_user('confirm_email_after_payment')
        payment = Payment(self.driver, payment_page)
        client_area_page = payment.make_single_payment_with_credit_card_with_full_registration(user)
        confirm_email(self.driver, user.email)

        self.assert_that_correct_email(client_area_page, user)

    def assert_that_correct_email(self, client_area_page, user):
        profile_page = client_area_page.open_profile_page()
        assert profile_page.correct_email(user)