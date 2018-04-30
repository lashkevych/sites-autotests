from selenium.webdriver.support.ui import Select

from site_autotest.settings import *
from site_autotest.utils import *
from selenium.common.exceptions import NoSuchElementException


class PaymentPage(object):
    def __init__(self, driver):
        self.driver = driver

    def make_payment_with_credit_card(self, plan, enter_email):
        if enter_email:
            self.enter_email()
        self.choose_plan(plan)
        self.select_cc_payment_method()
        self.enter_card_data()
        self.submit_purchase()

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
        Select(self.driver.find_elements_by_class_name('year-exp')[2].find_element_by_tag_name('select')
               ).select_by_visible_text(CARD_EXP_YEAR)

    def enter_month_exp(self):
        Select(self.driver.find_elements_by_class_name('month-exp')[2].find_element_by_tag_name('select')
               ).select_by_visible_text(CARD_EXP_MONTH)

    def enter_card_number(self):
        card_number_parts = CARD_NUMBER.split('-')
        self.driver.find_element_by_xpath("(//input[@id='cc-full-1'])[2]").click()
        self.driver.find_element_by_xpath("(//input[@id='cc-full-1'])[2]").send_keys(card_number_parts[0])
        self.driver.find_element_by_xpath("(//input[@id='cc-full-2'])[2]").send_keys(card_number_parts[1])
        self.driver.find_element_by_xpath("(//input[@id='cc-full-3'])[2]").send_keys(card_number_parts[2])
        self.driver.find_element_by_xpath("(//input[@id='cc-full-4'])[2]").send_keys(card_number_parts[3])

    def select_cc_payment_method(self):
        self.driver.find_element_by_class_name('stripe').click()

    def enter_email(self):
        email = generate_email()
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
        self.driver.find_element_by_xpath("//button[contains(@class, 'btn-purchase')]").click()

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

