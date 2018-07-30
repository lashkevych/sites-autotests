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

    def complete_registration(self, payment_page):
        complete_user_sign_up_page = payment_page.agree_complete_sign_up()
        return complete_user_sign_up_page.complete_user_sign_up()

    def get_last_plan(self, control_panel_page):
        profile_page = control_panel_page.open_profile_page()
        return profile_page.get_last_plan()

    def assert_that_plans_are_equal(self, purchased_plan, last_plan):
        assert purchased_plan.upper() == last_plan.upper()




    '''def test_single_payment_cc_by_existing_user_12m(self):
        plan = '12 Months'
        user = create_user('exist_user_12m')
        login_form = self.main_page.get_login_form()
        control_panel_page = login_form.login(user.username, user.password)
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, '', False, 'AmericanExpress_hypepay')
        control_panel_page = payment_page.agree_go_to_account()


    def test_single_payment_cc_incorrect_cvc(self):
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
        control_panel_page = payment_page.agree_go_to_account()

    def test_renewal_payment_cc_by_existing_user_same_card(self):
        plan = '1 Month'
        user = create_user('renewal_1m_12m_same_card')
        login_form = self.main_page.get_login_form()
        control_panel_page = login_form.login(user.username, user.password)
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, '', False, 'Visa_squareup')
        control_panel_page = payment_page.agree_go_to_account()
        plan = '12 Months'
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, '', False, 'Visa_squareup')
        control_panel_page = payment_page.agree_go_to_account()

    def test_renewal_payment_cc_by_existing_user_another_card(self):
        plan = '3 Months'
        user = create_user('renewal_3m_1m_another_card')
        login_form = self.main_page.get_login_form()
        control_panel_page = login_form.login(user.username, user.password)
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, '', False, 'Visa_squareup')
        control_panel_page = payment_page.agree_go_to_account()
        plan = '1 Month'
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, '', False, 'MasterCards_squareup')
        control_panel_page = payment_page.agree_go_to_account()'''

