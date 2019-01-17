from site_autotest.utils import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class PayPalPaymentPage(object):
    def __init__(self, driver, is_subscription):
        self.driver = driver

        if is_subscription:
            self.pay_pal_wait_for('Timed out waiting for Start Pay Pal Payment Page to load')

        '''if not is_subscription:
            method = EC.element_to_be_clickable((By.XPATH, "//input[@name='login_email']"))
        else:
            method = EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']//span[contains(text(),'Check out')]/ancestor::button[1]"))
        wait_for(self.driver, DELAY_FOR_PAY_PAL_PAGE, method,
                                 'Timed out waiting for Pay Pal Payment Page to load')
        '''

    def confirm_subscription(self):
        self.driver.find_element_by_xpath(
            "//button[@type='submit']//span[contains(text(),'Check out')]/ancestor::button[1]").click()

        self.pay_pal_wait_for('Timed out waiting for Login Pay Pal Payment Page to load')

    def enter_and_submit_pay_pal_creds(self):
        self.enter_pay_pal_email()
        self.enter_pay_pal_password()
        self.submit_pay_pal_creds()

        self.pay_pal_wait_for('Timed out waiting for Confirm Pay Pal Payment Page to load')

    def confirm_pay_pal_payment(self):
        # specific paypal algorithm - Sometime first form is shown, sometime - second, sometime - both
        # But I don't know algorithm
        try:
            self.driver.find_element_by_xpath("//button[contains(text(),'Continue')]").click()
        except:
            pass

        try:
            self.driver.find_element_by_xpath("//input[@data-test-id='continueButton']").click()
        except:
            pass

        self.pay_pal_wait_for('Timed out waiting for Return to Merchant Page to load')

    def return_to_merchant(self):
        self.driver.find_element_by_xpath("//input[@value='Return to Merchant']").click()
        self.pay_pal_wait_for('Timed out waiting for Pay pal redirect to Merchant Page')

    def enter_pay_pal_email(self):
        pay_pal_email_element = self.driver.find_element_by_xpath("//input[@name='login_email']")
        set_text(pay_pal_email_element, QA_PAY_PAL_EMAIL)

    def enter_pay_pal_password(self):
        pay_pal_password_element = self.driver.find_element_by_xpath("//input[@name='login_password']")
        set_text(pay_pal_password_element, QA_PAY_PAL_PASSWORD)

    def submit_pay_pal_creds(self):
        self.driver.find_element_by_xpath("//button[@value='Login']").click()

    def pay_pal_wait_for(self, message):
        method = EC.visibility_of_element_located((By.ID, "preloaderSpinner"))
        wait_for(self.driver, DELAY_FOR_PAY_PAL_PAGE, method,
                 message, False)

class PaymentPage(object):
    def __init__(self, driver):
        self.driver = driver

    def make_payment_with_pay_pal(self, plan, email_prefix, is_enter_email=True, is_subscription=False):
        if is_enter_email:
            self.enter_email(email_prefix)
        self.choose_plan(plan)
        self.select_pp_payment_method()
        if not is_subscription:
            self.uncheck_pp_subscription()
        self.submit_purchase()
        pay_pal_payment_page = PayPalPaymentPage(self.driver, is_subscription)
        if is_subscription:
            pay_pal_payment_page.confirm_subscription()
        pay_pal_payment_page.enter_and_submit_pay_pal_creds()
        pay_pal_payment_page.confirm_pay_pal_payment()
        pay_pal_payment_page.return_to_merchant()

    def select_pp_payment_method(self):
        self.driver.find_element_by_class_name('paypal').click()
        method = EC.visibility_of_element_located((By.CSS_SELECTOR, "label[for='enable-subscription']"))
        wait_for(self.driver, DELAY_FOR_PAY_PAL_PAGE, method,
                 "Timed out waiting for Pay Pal Payment Method Page to load")

    def uncheck_pp_subscription(self):
        self.driver.find_element_by_css_selector("label[for='enable-subscription']").click()

    def make_payment_with_credit_card(self, plan, email_prefix, is_enter_email=True, is_subscription=False,  card_type='Visa_hypepay'):
        if is_enter_email:
            self.enter_email(email_prefix)
        self.choose_plan(plan)
        self.select_cc_payment_method()
        if not is_subscription:
            self.uncheck_cc_subscription()
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
        from site_autotest.pages.client_area_page import ClientAreaPage
        self.driver.find_element_by_xpath("//div[contains(@class, 'signup')]//a[contains(@class, 'btn')]").click()
        client_area_page = ClientAreaPage(self.driver)

        return client_area_page

    def agree_complete_sign_up(self):
        from site_autotest.pages.user_sign_up_page import CompleteSignUpPage
        self.driver.find_element_by_xpath("//div[contains(@class, 'signup')]//a[contains(@class, 'btn')]").click()
        complete_signup_page = CompleteSignUpPage(self.driver)

        return complete_signup_page

    def not_agree_complete_sign_up(self, main_page):
        self.driver.find_element_by_css_selector("a.logo").click()

    def uncheck_cc_subscription(self):
        self.driver.find_element_by_xpath("//label[contains(@for, 'enable-subscription-checkbox')]").click()
