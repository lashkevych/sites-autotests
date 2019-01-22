import pytest
from site_autotest.pages.main_page import MainPage
from site_autotest.pages.payment_page import Payment
from Utils.emailR import AnonineEmailClientWrapper

from site_autotest.utils import *

def confirm_email(driver, user_email, subject):
    email_client_wrapper = AnonineEmailClientWrapper(QA_EMAIL, QA_EMAIL_PASSWORD)
    link_text = 'VERIFY MY EMAIL ADDRESS'
    confirm_email_link = email_client_wrapper.get_link(user_email, subject, link_text)
    if bool(confirm_email_link):
        script_open_window = "window.open('%s', 'new_window')" % confirm_email_link
    else:
        pytest.fail('there is no email to confirm')
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

        time.sleep(DELAY_BEFORE_GETTING_EMAILS)
        # TBD  - need optimization of email count

        confirm_email(self.driver, user.email, 'Thank you for your Interest in our Anonine Service!')

        self.assert_that_correct_email(client_area_page, user)


    def test_confirm_email_after_change_email_in_client_area(self):
        payment_page = self.main_page.open_payment_page()
        user = generate_user('confirm_email_after_change_email')
        payment = Payment(self.driver, payment_page)
        client_area_page = payment.make_single_payment_with_credit_card_with_full_registration(user)
        profile_page = client_area_page.open_profile_page()

        profile_page.go_to_change_email_tab()
        user_with_new_email =  User(username=user.username, password=user.password, email=generate_email('confirm_email_after_change_email'))
        profile_page.change_email(user_with_new_email.email)

        time.sleep(DELAY_BEFORE_GETTING_EMAILS)
        # TBD  - need optimization of email count

        confirm_email(self.driver, user_with_new_email.email, "Please Confirm your Email Address!")

        self.assert_that_correct_email(client_area_page, user_with_new_email)

    def assert_that_correct_email(self, client_area_page, user):
        profile_page = client_area_page.open_profile_page()
        assert profile_page.correct_email(user)