# -*- coding: utf-8 -*-
from time import sleep

import pytest
from site_autotest.pages.main_page import MainPage

from site_autotest.utils import *


class TestPayment(object):
    @pytest.fixture(autouse=True)
    def setup_method(self, driver_fixture, variables):
        self.driver = driver_fixture
        self.main_page = MainPage(self.driver, variables)
        self.main_page.open()

    def test_single_payment_cc_with_full_registration_1m(self):
        purchased_plan = '1 Month'
        payment_method = 'Inovio'
        email = generate_email('cc_full_reg_1m_single')
        payment_page = self.main_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, email, False, 'Visa_hypepay')
        client_area_page = self.complete_registration(payment_page)

        last_plan, last_payment_method = client_area_page.get_last_paid_plan_and_payment_method()
        self.assert_that_plans_are_equal(purchased_plan, last_plan)
        self.assert_that_payment_methods_are_equal(payment_method, last_payment_method)

    def test_single_payment_cc_with_full_registration_3m(self):
        purchased_plan = '3 Months'
        payment_method = 'Inovio'
        email = generate_email('cc_full_reg_3m_single')
        payment_page = self.main_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, email, False, 'MasterCards_hypepay')
        client_area_page = self.complete_registration(payment_page)

        last_plan, last_payment_method = client_area_page.get_last_paid_plan_and_payment_method()
        self.assert_that_plans_are_equal(purchased_plan, last_plan)
        self.assert_that_payment_methods_are_equal(payment_method, last_payment_method)

    def test_single_payment_cc_by_existing_user_12m(self):
        purchased_plan = '12 Months'
        payment_method = 'Inovio'
        client_area_page, _ = self.main_page.login_random_exist_user('cc_exist_user_12m_single')
        payment_page = client_area_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, None, False, 'AmericanExpress_hypepay')
        client_area_page = payment_page.agree_go_to_account()

        last_plan, last_payment_method = client_area_page.get_last_paid_plan_and_payment_method()
        self.assert_that_plans_are_equal(purchased_plan, last_plan)
        self.assert_that_payment_methods_are_equal(payment_method, last_payment_method)

    def test_subscription_payment_cc_by_existing_user_12m(self):
        purchased_plan = '12 Months'
        payment_method = 'Inovio'
        client_area_page, _ = self.main_page.login_random_exist_user('cc_exist_user_12m_sub')
        payment_page = client_area_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, None, True, 'Visa_hypepay')
        client_area_page = payment_page.agree_go_to_account()

        last_plan, last_payment_method = client_area_page.get_last_paid_plan_and_payment_method()
        self.assert_that_plans_are_equal(purchased_plan, last_plan)
        self.assert_that_payment_methods_are_equal(payment_method, last_payment_method)
        self.assert_that_exist_cc_subscription(client_area_page)

    def test_renewal_payment_cc_by_existing_user(self):
        purchased_plan = '3 Months'
        payment_method = 'Inovio'
        client_area_page, _ = self.main_page.login_random_exist_user('cc_renewal_single_3m_sub_1m')
        payment_page = client_area_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, None, False, 'Visa_hypepay')
        client_area_page = payment_page.agree_go_to_account()

        last_plan, last_payment_method = client_area_page.get_last_paid_plan_and_payment_method()
        self.assert_that_plans_are_equal(purchased_plan, last_plan)
        self.assert_that_payment_methods_are_equal(payment_method, last_payment_method)

        purchased_plan = '1 Month'
        payment_page = client_area_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, None, True, 'MasterCards_hypepay')
        client_area_page = payment_page.agree_go_to_account()

        last_plan, last_payment_method = client_area_page.get_last_paid_plan_and_payment_method()
        self.assert_that_plans_are_equal(purchased_plan, last_plan)
        self.assert_that_payment_methods_are_equal(payment_method, last_payment_method)
        self.assert_that_exist_cc_subscription(client_area_page)

    def test_single_payment_cc_with_NOT_full_registration_1m(self):
        purchased_plan = '1 Month'
        email = generate_email('cc_NOT-full_reg_1m_single')
        payment_page = self.main_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, email, False, 'Visa_hypepay')
        client_area_page = self.not_complete_registration(payment_page)

        self.assert_that_logged_user_is_no_creds(client_area_page)

    def test_sub_payment_pp_with_full_registration_1m(self):
        purchased_plan = '1 Month'
        email = generate_email('pp_full_reg_1m_sub')
        payment_page = self.main_page.open_payment_page()

        payment_page.make_payment_with_pay_pal(purchased_plan, email, True)
        client_area_page = self.complete_registration(payment_page)

        # registration of PayPal payment on the backend takes about 20-30 minutes ->
        # we do not wait for the end of this registration ->
        # we check only if the payment process is completed successfully
        self.assert_that_payment_is_finished_successfully(client_area_page)

        #last_plan, last_payment_method = client_area_page.get_last_paid_plan_and_payment_method()
        #payment_method = 'Paypal'
        #self.assert_that_plans_are_equal(purchased_plan, last_plan)
        #self.assert_that_payment_methods_are_equal(payment_method, last_payment_method)


    def test_single_payment_pp_with_full_registration_1m(self):
        purchased_plan = '1 Month'
        payment_method = 'Paypal'
        email = generate_email('pp_full_reg_1m_single')
        payment_page = self.main_page.open_payment_page()

        payment_page.make_payment_with_pay_pal(purchased_plan, email, False)
        client_area_page = self.complete_registration(payment_page)

        # registration of PayPal payment on the backend takes about 20-30 minutes ->
        # we do not wait for the end of this registration ->
        # we check only if the payment process is completed successfully

        last_plan, last_payment_method = client_area_page.get_last_paid_plan_and_payment_method()
        self.assert_that_plans_are_equal(purchased_plan, last_plan)
        self.assert_that_payment_methods_are_equal(payment_method, last_payment_method)


    def test_renewal_single_payment_pp_by_existing_user(self):
        purchased_plan = '3 Months'
        payment_method = 'Inovio'

        client_area_page, _ = self.main_page.login_random_exist_user('renewal_single_3m_cc_single_1m_pp')
        payment_page = client_area_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, None, False, 'Visa_hypepay')
        client_area_page = payment_page.agree_go_to_account()

        last_plan, last_payment_method = client_area_page.get_last_paid_plan_and_payment_method()
        self.assert_that_plans_are_equal(purchased_plan, last_plan)
        self.assert_that_payment_methods_are_equal(payment_method, last_payment_method)

        purchased_plan = '1 Month'
        payment_method = 'Paypal'
        payment_page = client_area_page.open_payment_page()

        payment_page.make_payment_with_pay_pal(purchased_plan, None, False)
        client_area_page = payment_page.agree_go_to_account()

        # sleep should be changed to using function wait_for  - in all test
        #time.sleep(DELAY_BEFORE_GETTING_EMAILS*3)
        last_plan, last_payment_method = client_area_page.get_last_paid_plan_and_payment_method(2)
        self.assert_that_plans_are_equal(purchased_plan, last_plan)
        self.assert_that_payment_methods_are_equal(payment_method, last_payment_method)

    def complete_registration(self, payment_page):
        complete_user_sign_up_page = payment_page.agree_complete_sign_up()
        return complete_user_sign_up_page.complete_user_sign_up()

    def not_complete_registration(self, payment_page):
        payment_page.not_agree_complete_sign_up()
        return self.main_page.open_client_area_page()

    def assert_that_plans_are_equal(self, purchased_plan, last_plan):
        assert purchased_plan.upper() == last_plan.upper()

    def assert_that_payment_methods_are_equal(self, payment_method, last_payment_method):
        assert payment_method.upper() == last_payment_method.upper()

    def assert_that_exist_cc_subscription(self, client_area_page):
        profile_page = client_area_page.open_profile_page()
        assert profile_page.exist_cc_subscription()

    def assert_that_exist_pp_subscription(self, client_area_page):
        profile_page = client_area_page.open_profile_page()
        assert profile_page.exist_pp_subscription()

    def assert_that_logged_user_is_no_creds(self,client_area_page):
        profile_page = client_area_page.open_profile_page_no_creds_user()
        assert profile_page.is_user_no_creds()

    def assert_that_payment_is_finished_successfully(self, client_area_page):
        assert client_area_page.is_registration_process_finished_successfully()
