from time import sleep

from selenium.webdriver.support.ui import Select

from site_autotest.settings import *
from site_autotest.utils import *
from selenium.common.exceptions import NoSuchElementException


class PaymentPage(object):
    def __init__(self, driver):
        self.driver = driver

    def make_payment_with_credit_card(self, plan, email_prefix, enter_email=True, card_name='Visa_stripe'):
        if enter_email:
            self.enter_email(email_prefix)
        self.choose_plan(plan)
        self.select_cc_payment_method()
        self.enter_card_data(CARDS[card_name])
        self.submit_purchase()

    def enter_card_data(self, card):
        self.enter_card_number(card.number)
        self.enter_exp_date(card.exp_month, card.exp_year)
        self.enter_cvc_code(card.cvc_code)
        self.enter_zip_postal_code(card.zip_postal_code)

    def enter_zip_postal_code(self, zip_postal_code):
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector("iframe[id='square-iframe']"))
        sleep(DELAY_BETWEEN_ATTEMPTS)
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector("iframe[id='sq-postal-code']"))
        zip_postal_code_element = self.driver.find_element_by_xpath("//input")
        set_text(zip_postal_code_element, zip_postal_code)
        self.driver.switch_to.default_content()
        #zip_postal_code_element = self.driver.find_elements_by_xpath("(//input[contains(@class, 'address_zip')])")[2]

    def enter_cvc_code(self, cvc_code):
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector("iframe[id='square-iframe']"))
        sleep(DELAY_BETWEEN_ATTEMPTS)
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector("iframe[id='sq-cvv']"))
        cvc_code_element = self.driver.find_element_by_xpath("//input")
        set_text(cvc_code_element, cvc_code)
        self.driver.switch_to.default_content()
        #cvc_code_element = self.driver.find_elements_by_xpath("(//input[contains(@class, 'cvc')])")[2]

    def enter_exp_date(self, exp_month, exp_year):
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector("iframe[id='square-iframe']"))
        sleep(DELAY_BETWEEN_ATTEMPTS)
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector("iframe[id='sq-expiration-date']"))
        exp_date_element = self.driver.find_element_by_xpath("//input")
        exp_date = exp_month + exp_year
        set_text(exp_date_element, exp_date)
        self.driver.switch_to.default_content()

    """
    def enter_year_exp(self, exp_year):
        Select(self.driver.find_elements_by_class_name('year-exp')[2].find_element_by_tag_name('select')
               ).select_by_visible_text(exp_year)

    def enter_month_exp(self, exp_month):
        Select(self.driver.find_elements_by_class_name('month-exp')[2].find_element_by_tag_name('select')
               ).select_by_visible_text(exp_month)
    """

    def enter_card_number(self, card_number):
        """
        card_number_parts = card_number.split('-')
        self.driver.find_element_by_xpath("(//input[@id='cc-full-1'])[2]").click()
        self.driver.find_element_by_xpath("(//input[@id='cc-full-1'])[2]").send_keys(card_number_parts[0])
        self.driver.find_element_by_xpath("(//input[@id='cc-full-2'])[2]").send_keys(card_number_parts[1])
        self.driver.find_element_by_xpath("(//input[@id='cc-full-3'])[2]").send_keys(card_number_parts[2])
        self.driver.find_element_by_xpath("(//input[@id='cc-full-4'])[2]").send_keys(card_number_parts[3])
        """
        #get_attribute("attribute name")
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector("iframe[id='square-iframe']"))
        sleep(DELAY_BETWEEN_ATTEMPTS)
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector("iframe[id='sq-card-number']"))
        card_number_element = self.driver.find_element_by_xpath("//input")
        set_text(card_number_element, card_number)
        self.driver.switch_to.default_content()

    def select_cc_payment_method(self):
        self.driver.find_element_by_class_name('square').click()

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

