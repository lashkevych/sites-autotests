from time import sleep

from selenium.webdriver.support.ui import Select

from site_autotest.settings import *
from site_autotest.utils import *
from selenium.common.exceptions import NoSuchElementException


class PaymentPage(object):
    def __init__(self, driver):
        self.driver = driver

    def make_payment_with_credit_card(self, plan, email_prefix, is_enter_email=True, is_subscription=False,  card_type='Visa_hypepay'):
        if is_enter_email:
            self.enter_email(email_prefix)
        self.choose_plan(plan)
        self.select_cc_payment_method()
        if not is_subscription:
            self.uncheck_subscription()
        random_card = generate_random_card(card_type)
        self.enter_card_data(random_card)
        self.submit_purchase()

    def enter_card_data(self, card):
        self.enter_card_number(card.number)
        self.enter_exp_date(card.exp_month, card.exp_year)
        self.enter_cvc_code(card.cvc_code)
        self.enter_zip_postal_code(card.zip_postal_code)

    def enter_zip_postal_code(self, zip_postal_code):
        zip_postal_code_element = self.driver.find_element_by_xpath("//input[@id='card-zip-code']")
        set_text(zip_postal_code_element, zip_postal_code)

    def enter_cvc_code(self, cvc_code):
        cvc_code_element = self.driver.find_element_by_xpath("//input[@placeholder='CVC']")
        set_text(cvc_code_element, cvc_code)

    def enter_exp_date(self, exp_month, exp_year):
        exp_date_element = self.driver.find_element_by_xpath("//input[@id='exp-date']")
        exp_date = exp_month + exp_year
        set_text(exp_date_element, exp_date)

    def enter_card_number(self, card_number):
        card_number_element = self.driver.find_element_by_xpath("//input[@id='card-number']")
        set_text(card_number_element, card_number)

    def select_cc_payment_method(self):
        self.driver.find_element_by_class_name('hypepay').click()

    def enter_email(self, email_prefix):
        email = generate_email(email_prefix)
        input_email_el = self.driver.find_element_by_xpath("//div[contains(@id, 'email-entry')]//input[@type='text']")
        set_text(input_email_el, email)

    def choose_plan(self,plan):
        plans = self.driver.find_elements_by_xpath(
            "//div[contains(@class, 'plans-select')]//div[contains(@class, 'plan')]")
        for plan_el in plans:
            if plan_el.find_element_by_class_name('month').text == plan:
                plan_el.click()
                break
        else:
            raise Exception("Can't find %s plan" % plan)

    def submit_purchase(self):
        self.driver.find_element_by_xpath("//button[contains(@class, 'card-v2__btn-purchase')]").click()

    def agree_go_to_account(self):
        from site_autotest.pages.control_panel import ControlPanelPage
        self.driver.find_element_by_xpath("//div[contains(@class, 'signup')]//a[contains(@class, 'btn')]").click()
        return ControlPanelPage(self.driver)

    def agree_complete_sign_up(self):
        from site_autotest.pages.user_sign_up import CompleteSignUpPage
        self.driver.find_element_by_xpath("//div[contains(@class, 'signup')]//a[contains(@class, 'btn')]").click()
        return CompleteSignUpPage(self.driver)


    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def uncheck_subscription(self):
        self.driver.find_element_by_xpath("//label[contains(@for, 'enable-subscription-checkbox')]").click()

#get_attribute("attribute name")