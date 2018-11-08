
import pytest
from site_autotest.utils import wait_for
from site_autotest.config import TEST_RESELLER
from site_autotest.settings import DELAY_FOR_LOADING_PAGE
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ProfilePage(object):
    def __init__(self, driver):
        self.driver = driver

    def get_last_paid_plan(self):
        return self.driver.find_element_by_xpath("//table[@class = 'table-history-body']/tbody/tr[1]/td[2]").text

    def get_last_payment_method(self):
        return self.driver.find_element_by_xpath("//table[@class = 'table-history-body']/tbody/tr[1]/td[4]").text

    def exist_cc_subscription(self):
        if self.driver.find_element_by_xpath("//a[@id='cancel_inovio_subscription']"):
            return True
        else:
            return False

    def exist_pp_subscription(self):
        if self.driver.find_element_by_xpath("//a[@href='https://www.paypal.com/']"):
            return True
        else:
            return False

    def user_is_no_creds(self):
        if self.driver.find_element_by_xpath("//input[@id='username']"):
            return True
        else:
            return False

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

    def get_last_paid_plan_and_payment_method(self):
        profile_page = self.open_profile_page()
        return (profile_page.get_last_paid_plan(),profile_page.get_last_payment_method())

    def exist_logout_link(self):
        try:
            if TEST_RESELLER == 'anonine':
                self.driver.find_element_by_xpath("//a[@href='/en/logout']")
            elif TEST_RESELLER == 'box-pn':
                self.driver.find_element_by_xpath("//a[@href='/logout']")
            else:
                pytest.fail('Unknown reseller in check if exist logout link')
            return True
        except:
            return False