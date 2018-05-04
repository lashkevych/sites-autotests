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
        plan = '1 Month'
        payment_page = self.main_page.open_payment_page()
        payment_page.make_payment_with_credit_card(plan, 'full_reg_1m', True, 'Visa_squareup')
        complete_user_sign_up_page = payment_page.agree_complete_sign_up()
        control_panel_page = complete_user_sign_up_page.complete_user_sign_up()
        pass

    def test_single_payment_cc_with_full_registration_3m(self):
        plan = '3 Months'
        payment_page = self.main_page.open_payment_page()
        payment_page.make_payment_with_credit_card(plan, 'full_reg_3m', True, 'MasterCards_squareup')
        complete_user_sign_up_page = payment_page.agree_complete_sign_up()
        control_panel_page = complete_user_sign_up_page.complete_user_sign_up()
        pass

        # div class = flash-message-success  and text = Your username and password have been set!

    def test_single_payment_cc_by_existing_user_12m(self):
        plan = '12 Months'
        user = create_user('exist_user_12m')
        login_form = self.main_page.open_login_form()
        control_panel_page = login_form.login(user.username, user.password)
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, '', False, 'AmericanExpress_squareup')
        control_panel_page = payment_page.agree_go_to_account()


    def test_single_payment_cc_incorrect_cvc(self):
        plan = '12 Months'
        user = create_user('incorrect-cvc_12m')
        login_form = self.main_page.open_login_form()
        control_panel_page = login_form.login(user.username, user.password)
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, "", False, 'Visa_squareup_incorrect_cvc')
        control_panel_page = payment_page.agree_go_to_account()

    def test_single_payment_cc_incorrect_zip(self):
        plan = '12 Months'
        user = create_user('incorrect-zip_12m')
        login_form = self.main_page.open_login_form()
        control_panel_page = login_form.login(user.username, user.password)
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, "", False, 'Visa_squareup_incorrect_zip')
        control_panel_page = payment_page.agree_go_to_account()

    def test_single_payment_cc_incorrect_exp_date(self):
        plan = '12 Months'
        user = create_user('incorrect-exp_date_12m')
        login_form = self.main_page.open_login_form()
        control_panel_page = login_form.login(user.username, user.password)
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, "", False, 'Visa_squareup_incorrect_exp_date')
        control_panel_page = payment_page.agree_go_to_account()

    def test_renewal_payment_cc_by_existing_user_same_card(self):
        plan = '1 Month'
        user = create_user('renewal_1m_12m_same_card')
        login_form = self.main_page.open_login_form()
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
        login_form = self.main_page.open_login_form()
        control_panel_page = login_form.login(user.username, user.password)
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, '', False, 'Visa_squareup')
        control_panel_page = payment_page.agree_go_to_account()
        plan = '1 Month'
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, '', False, 'MasterCards_squareup')
        control_panel_page = payment_page.agree_go_to_account()


    def assert_that_logout_link_exist(self):
        self.driver.find_element_by_xpath("//a[@href='/en/logout']")