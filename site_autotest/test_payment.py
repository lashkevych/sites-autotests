# -*- coding: utf-8 -*-
import pytest
from site_autotest.pages.main import MainPage

from site_autotest.utils import *


class TestPayment(object):
    @pytest.fixture(autouse=True)
    def setup_method(self, selenium):
        self.driver = selenium
        self.main_page = MainPage(self.driver)
        self.main_page.open()

    def test_payment_credit_card_with_full_registration(self):
        plan = "1 Month"
        payment_page = self.main_page.open_payment_page()
        payment_page.make_payment_with_credit_card(plan, enter_email=True)
        complete_user_sign_up_page = payment_page.agree_complete_sign_up()
        control_panel_page = complete_user_sign_up_page.complete_user_sign_up()
        pass

        # div class = flash-message-success  and text = Your username and password have been set!

    def test_payment_credit_card_by_existing_user(self):
        plan = "3 Months"
        user = create_user()
        login_form = self.main_page.open_login_form()
        control_panel_page = login_form.login(user.username, user.password)
        payment_page = control_panel_page.open_upgrade_page()
        payment_page.make_payment_with_credit_card(plan, enter_email=False)
        control_panel_page = payment_page.agree_go_to_account()

    def assert_that_logout_link_exist(self):
        self.driver.find_element_by_xpath("//a[@href='/en/logout']")