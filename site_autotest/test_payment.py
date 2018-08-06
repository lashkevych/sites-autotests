# -*- coding: utf-8 -*-
from time import sleep

import pytest
from site_autotest.pages.main import MainPage
from site_autotest.settings import DELAY_BETWEEN_ATTEMPTS

from site_autotest.utils import *


class TestPayment(object):
    @pytest.fixture(autouse=True)
    def setup_method(self, selenium):
        self.driver = selenium
        self.main_page = MainPage(self.driver)
        self.main_page.open()

    def test_single_payment_cc_with_full_registration_1m(self):
        purchased_plan = '1 Month'
        payment_page = self.main_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, 'full_reg_1m_single', True, False, 'Visa_hypepay')
        control_panel_page = self.complete_registration(payment_page)

        self.assert_that_plans_are_equal(purchased_plan, self.get_last_plan(control_panel_page))

    def test_single_payment_cc_with_full_registration_3m(self):
        purchased_plan = '3 Months'
        payment_page = self.main_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, 'full_reg_3m_single', True, False, 'MasterCards_hypepay')
        control_panel_page = self.complete_registration(payment_page)

        self.assert_that_plans_are_equal(purchased_plan, self.get_last_plan(control_panel_page))

    def test_single_payment_cc_by_existing_user_12m(self):
        purchased_plan = '12 Months'
        control_panel_page = self.login_random_exist_user('exist_user_12m_single')
        payment_page = control_panel_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, '', False, False, 'AmericanExpress_hypepay')
        control_panel_page = payment_page.agree_go_to_account()

        self.assert_that_plans_are_equal(purchased_plan, self.get_last_plan(control_panel_page))

    def test_subscription_payment_cc_by_existing_user_12m(self):
        purchased_plan = '12 Months'
        control_panel_page = self.login_random_exist_user('exist_user_12m_sub')
        payment_page = control_panel_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, '', False, True, 'Visa_hypepay')
        control_panel_page = payment_page.agree_go_to_account()

        self.assert_that_plans_are_equal(purchased_plan, self.get_last_plan(control_panel_page))
        self.assert_that_exist_subscription(control_panel_page)

    def test_renewal_payment_cc_by_existing_user(self):
        purchased_plan = '3 Months'
        control_panel_page = self.login_random_exist_user('renewal_single_3m_sub_1m')
        payment_page = control_panel_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, '', False, False, 'Visa_hypepay')
        control_panel_page = payment_page.agree_go_to_account()

        self.assert_that_plans_are_equal(purchased_plan, self.get_last_plan(control_panel_page))

        purchased_plan = '1 Month'
        payment_page = control_panel_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, '', False, True, 'MasterCards_hypepay')
        control_panel_page = payment_page.agree_go_to_account()

        self.assert_that_plans_are_equal(purchased_plan, self.get_last_plan(control_panel_page))
        self.assert_that_exist_subscription(control_panel_page)

    def test_single_payment_cc_with_NOT_full_registration_1m(self):
        purchased_plan = '1 Month'
        payment_page = self.main_page.open_payment_page()

        payment_page.make_payment_with_credit_card(purchased_plan, 'NOT-full_reg_1m_single', True, False, 'Visa_hypepay')
        control_panel_page = self.not_complete_registration(payment_page)

        self.assert_that_logged_user_is_no_creds(control_panel_page)

    def complete_registration(self, payment_page):
        complete_user_sign_up_page = payment_page.agree_complete_sign_up()
        return complete_user_sign_up_page.complete_user_sign_up()

    def not_complete_registration(self, payment_page):
        payment_page.not_agree_complete_sign_up()
        return self.main_page.open_client_area_page()

    def get_last_plan(self, control_panel_page):
        profile_page = control_panel_page.open_profile_page()
        return profile_page.get_last_plan()

    def login_random_exist_user (self, email_prefix):
        user = create_user(email_prefix)
        login_form = self.main_page.get_login_form()
        return login_form.login(user.username, user.password)

    def login_exist_user (self, user):
        login_form = self.main_page.get_login_form()
        return login_form.login(user.username, user.password)

    def assert_that_plans_are_equal(self, purchased_plan, last_plan):
        assert purchased_plan.upper() == last_plan.upper()

    def assert_that_exist_subscription(self,control_panel_page):
        profile_page = control_panel_page.open_profile_page()
        assert profile_page.exist_subscription()

    def assert_that_logged_user_is_no_creds(self,control_panel_page):
        profile_page = control_panel_page.open_profile_page_no_creds_user()
        assert profile_page.user_is_no_creds()

    '''def test_single_payment_cc_incorrect_cvc(self):
        plan = '12 Months'
        user = create_user('incorrect-cvc_12m')
        login_form = self.main_page.get_login_form()
        control_panel_page = login_form.login(user.username, user.password)
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, "", False, 'Visa_squareup_incorrect_cvc')
        control_panel_page = payment_page.agree_go_to_account()

    def test_single_payment_cc_incorrect_zip(self):
        plan = '12 Months'
        user = create_user('incorrect-zip_12m')
        login_form = self.main_page.get_login_form()
        control_panel_page = login_form.login(user.username, user.password)
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, "", False, 'Visa_squareup_incorrect_zip')
        control_panel_page = payment_page.agree_go_to_account()

    def test_single_payment_cc_incorrect_exp_date(self):
        plan = '12 Months'
        user = create_user('incorrect-exp_date_12m')
        login_form = self.main_page.get_login_form()
        control_panel_page = login_form.login(user.username, user.password)
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, "", False, 'Visa_squareup_incorrect_exp_date')
        control_panel_page = payment_page.agree_go_to_account()'''



