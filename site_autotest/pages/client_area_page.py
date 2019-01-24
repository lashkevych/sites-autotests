
import pytest
from site_autotest.config import TEST_RESELLER
from site_autotest.utils import set_text
from site_autotest.settings import MAXIMUM_ATTEMPTS_OF_CHECKING_PAY_PAL_REGISTRATION
from site_autotest.settings import DELAY_BETWEEN_ATTEMPTS_OF_CHECKING_PAY_PAL_REGISTRATION
from selenium.common.exceptions import NoSuchElementException
import time


class ProfilePage(object):
    def __init__(self, driver):
        self.driver = driver

    def go_to_change_email_password_tab(self):
        self.driver.find_element_by_css_selector("a[data-name='changepass']").click()

    def change_password(self, new_password):
        self.enter_password(new_password)
        self.enter_confirm_password(new_password)
        self.submit_password()

    def enter_password(self,new_password):
        password_element = self.driver.find_element_by_id("password")
        set_text(password_element, new_password)

    def enter_confirm_password(self,new_password):
        password_element = self.driver.find_element_by_id("passconfirm")
        set_text(password_element, new_password)

    def submit_password(self):
        self.driver.find_element_by_css_selector("input[value='Save password']").click()

    def change_email(self, new_email):
        self.enter_email(new_email)
        self.submit_email()

    def enter_email(self,new_email):
        email_element = self.driver.find_element_by_id("new_email")
        set_text(email_element, new_email)

    def submit_email(self):
        self.driver.find_element_by_css_selector("input[value='Save email']").click()

    def get_last_paid_plan(self):
        return self.driver.find_element_by_xpath("//table[@class = 'table-history-body']/tbody/tr[2]/td[2]").text

    def get_last_payment_method(self):
        return self.driver.find_element_by_xpath("//table[@class = 'table-history-body']/tbody/tr[2]/td[4]").text

    def exist_such_number_of_payments(self, number_of_payments):
        path_str = "//table[@class = 'table-history-body']/tbody/tr[%s]/td[2]"%str(number_of_payments+1)
        self.driver.find_element_by_xpath(path_str)
        return True

    def exist_cc_subscription(self):
        self.driver.find_element_by_xpath("//a[@id='cancel_inovio_subscription']")
        return True

    def exist_pp_subscription(self):
        self.driver.find_element_by_xpath("//a[@href='https://www.paypal.com/']")
        return True

    def is_user_no_creds(self):
        self.driver.find_element_by_xpath("//input[@id='username']")
        return True

    def is_available_resend_button(self):
        self.driver.find_element_by_class("resend-email")
        return True

    def is_email_correct(self, user):
        str_for_find_username = "//b[text()='%s']" % user.username
        self.driver.find_element_by_xpath(str_for_find_username)

        str_for_find_email = "//b[text()='%s']"% user.email
        self.driver.find_element_by_xpath(str_for_find_email)
        return True


class ClientAreaPage(object):
    def __init__(self, driver):
        self.driver = driver

    def open_payment_page(self):
        from site_autotest.pages.payment_page import PaymentPage
        self.driver.find_element_by_partial_link_text('UPGRADE').click()
        payment_page = PaymentPage(self.driver)

        return payment_page

    def open_profile_page(self):
        el = self.driver.find_element_by_class_name('dashboard-content')
        el.find_element_by_partial_link_text('PROFILE').click()
        profile_page = ProfilePage(self.driver)

        return profile_page

    def open_profile_page_no_creds_user(self):
        el = self.driver.find_element_by_xpath("//a//div[text()='Profile']")
        el = el.find_element_by_xpath('..')
        el.click()
        profile_page = ProfilePage(self.driver)

        return profile_page

    def get_last_paid_plan_and_payment_method(self, number_of_payments = 1):
        profile_page = self.open_profile_page()

        for x in range(MAXIMUM_ATTEMPTS_OF_CHECKING_PAY_PAL_REGISTRATION):
            try:
                profile_page.exist_such_number_of_payments(number_of_payments)
                break
            except:
                if x == MAXIMUM_ATTEMPTS_OF_CHECKING_PAY_PAL_REGISTRATION-1:
                    #raise
                    pytest.fail("Last payment is not registered")
                time.sleep(DELAY_BETWEEN_ATTEMPTS_OF_CHECKING_PAY_PAL_REGISTRATION)
                self.driver.refresh()
        return (profile_page.get_last_paid_plan(), profile_page.get_last_payment_method())

    def go_to_main_page(self):
        self.driver.find_element_by_css_selector("a.logo").click()

    def logout(self):
        el = self.driver.find_element_by_class_name('dashboard-content')
        el.find_element_by_partial_link_text('LOG OUT').click()

    def exist_logout_link(self):
        try:
            if TEST_RESELLER == 'anonine':
                el = self.driver.find_element_by_class_name('dashboard-content')
                el.find_element_by_partial_link_text('LOG OUT')
            else:
                pytest.fail('Unknown reseller in check if exist logout link')
            return True
        except:
            return False

    def is_registration_process_finished_successfully(self):
        self.driver.find_element_by_class_name('flash-message-success')
        return  True