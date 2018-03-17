# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest

from site_autotest.utils import set_text, unique_number
from .settings import *


class Payment(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(WAIT_TIMEOUT)
        self.verificationErrors = []
        self.accept_next_alert = True

    def generate_username(self):
        return "test_user_%s" % unique_number()

    def test_payment_stripe(self):
        plan = "1 Month"
        self.go_to_payment_page()
        self.plan = self.choose_plan(plan)
        self.enter_email()
        self.select_payment_method()
        self.enter_card_data()
        self.submit_purchase()
        self.confirm_complete_sign_up()
        self.enter_username()
        self.enter_and_confirm_password()
        self.submit_creds()
        pass
        # div class = flash-message-success  and text = Your username and password have been set!

    def submit_creds(self):
        self.driver.find_element_by_xpath("//button[@type='submit']").click()

    def enter_and_confirm_password(self):
        password = TEST_PASSWORD
        password_element = self.driver.find_element_by_id("new-password1")
        set_text(password_element, password)
        confirm_password_element = self.driver.find_element_by_id("new-password2")
        set_text(confirm_password_element, password)

    def enter_username(self):
        username = self.generate_username()
        username_element = self.driver.find_element_by_id("username")
        set_text(username_element, username)

    def confirm_complete_sign_up(self):
        self.driver.find_element_by_xpath("//div[contains(@class, 'signup')]//a[contains(@class, 'btn')]").click()


    def submit_purchase(self):
        self.driver.find_element_by_xpath("//button[contains(@class, 'btn-purchase')]").click()

    def enter_card_data(self):
        self.enter_card_number()
        self.enter_month_exp()
        self.enter_year_exp()
        self.enter_cvc_code()
        self.enter_zip_postal_code()

    def enter_zip_postal_code(self):
        zip_postal_code = ZIP_POSTAL_CODE
        zip_postal_code_element = self.driver.find_elements_by_xpath("(//input[contains(@class, 'address_zip')])")[2]
        set_text(zip_postal_code_element, zip_postal_code)

    def enter_cvc_code(self):
        cvc_code = CARD_CVC_CODE
        cvc_code_element = self.driver.find_elements_by_xpath("(//input[contains(@class, 'cvc')])")[2]
        set_text(cvc_code_element, cvc_code)

    def enter_year_exp(self):
        #self.driver.find_element_by_xpath(
         #   "(//div[@id='card-entry']/div/div[2]/div/div/div[2]/p/span[4]/span/select)[2]").click()
        Select(self.driver.find_elements_by_class_name('year-exp')[2].find_element_by_tag_name('select')
               ).select_by_visible_text(CARD_EXP_YEAR)
        #self.driver.find_element_by_xpath("(//option[@value='2019'])[3]").click()

    def enter_month_exp(self):
        #self.driver.find_element_by_xpath(
        #    "(//div[@id='card-entry']/div/div[2]/div/div/div[2]/p/span[2]/span/select)[2]").click()
        Select(self.driver.find_elements_by_class_name('month-exp')[2].find_element_by_tag_name('select')
               ).select_by_visible_text(CARD_EXP_MONTH)
        #self.driver.find_element_by_xpath("(//option[@value='03'])[3]").click()

    def enter_card_number(self):
        #self.driver.find_element_by_id("cc-full-1").click()
        #self.driver.find_element_by_id("cc-full-1").send_keys('4242')
        card_number_parts = CARD_NUMBER.split('-')
        self.driver.find_element_by_xpath("(//input[@id='cc-full-1'])[2]").click()
        self.driver.find_element_by_xpath("(//input[@id='cc-full-1'])[2]").send_keys(card_number_parts[0])
        self.driver.find_element_by_xpath("(//input[@id='cc-full-2'])[2]").send_keys(card_number_parts[1])
        self.driver.find_element_by_xpath("(//input[@id='cc-full-3'])[2]").send_keys(card_number_parts[2])
        self.driver.find_element_by_xpath("(//input[@id='cc-full-4'])[2]").send_keys(card_number_parts[3])

    def select_payment_method(self):
        self.driver.find_element_by_class_name('stripe').click()

    def enter_email(self):
        email = self.generate_email()
        input_email_el = self.driver.find_element_by_xpath("//div[contains(@id, 'email-entry')]//input[@type='text']")
        set_text(input_email_el, email)

    def generate_email(self):
        email = USER_EMAIL_TEMPLATE % unique_number()
        return email

    def choose_plan(self,plan):
        plans = self.driver.find_elements_by_xpath(
            "//div[contains(@class, 'plans-select')]//div[contains(@class, 'plan')]")
        for plan_el in plans:
            if plan_el.find_element_by_class_name('month').text == plan:
                plan_el.click()
                break
        else:
            raise Exception("Can't find %s plan" % plan)

    def go_to_main_page(self):
        self.driver.get(SITE_URL)


    def go_to_payment_page(self):
        self.go_to_main_page()
        self.driver.find_element_by_link_text("BUY").click()


    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()