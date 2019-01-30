import pytest

from site_autotest.config import *
from site_autotest.utils import click_with_waiting_page_reload, create_user
from site_autotest.settings import SITE_URL_WITH_BASIC_AUTH, SITE_URL_NO_BASIC_AUTH, SUBJECT_OF_RESET_PASSWORD_EMAIL, \
    LINK_TEXT_FOR_RESET_PASSWORD_EMAIL
from site_autotest.pages.client_area_page import ClientAreaPage
from site_autotest.pages.payment_page import PaymentPage
from Utils.emailR import AnonineEmailClientWrapper
from site_autotest.pages.support_page import AnonineContactPage

class MainPage(object):
    def __init__(self, driver, variables):
        self.driver = driver
        self.variables = variables

    def open(self):
        if self.variables.get('use-basic-auth', True):
            self.driver.get(SITE_URL_WITH_BASIC_AUTH)
        else:
            if TEST_RESELLER == 'anonine':
                site_url = SITE_URL_NO_BASIC_AUTH + '/en/logout'
            elif TEST_RESELLER == 'box-pn':
                site_url = SITE_URL_NO_BASIC_AUTH + '/logout'
            else:
                pytest.fail('unknown reseller in open main page')
            self.driver.get(site_url)

    def open_payment_page(self):
        if TEST_RESELLER == 'anonine':
            self.driver.find_element_by_css_selector("a[data-test='pricing']").click()
            payment_page = PaymentPage(self.driver)
            return payment_page
        else:
            pytest.fail('Unknown reseller in open order page')

    def open_client_area_page(self):
        if TEST_RESELLER == 'anonine':
            method = lambda: self.driver.find_element_by_css_selector("a[data-test='sign-in']")
            click_with_waiting_page_reload(method)
            client_area_page = ClientAreaPage(self.driver)
            return client_area_page

        else:
            pytest.fail('Unknown reseller in open client area page')

    def open_login_page(self):
        if TEST_RESELLER == 'anonine':
            self.driver.find_element_by_css_selector("a[data-test='sign-in']").click()
            login_page = AnonineLoginPage(self.driver)
            return login_page
        else:
            pytest.fail('Unknown reseller in open login page')

    def login_random_exist_user(self, email_prefix):
        user = create_user(email_prefix)
        login_form = self.open_login_page()
        return login_form.login(user.username, user.password), user

    def login_exist_user(self, user):
        login_form = self.open_login_page()
        return login_form.login(user.username, user.password)


    def open_contact_page(self):
        if TEST_RESELLER == 'anonine':
            self.driver.find_element_by_css_selector("a[data-test='footer-link-company-Contact us']").click()
            contact_page = AnonineContactPage(self.driver)
            return contact_page
        else:
            pytest.fail('Unknown reseller in open login page')

    def get_new_password_page(self):
        if TEST_RESELLER == 'anonine':
            return AnonineEnterNewPasswordPage(self.driver)
        else:
            pytest.fail('Unknown reseller in get new password page')


    def exist_logout_link(self):
        if TEST_RESELLER == 'anonine':
            self.driver.find_element_by_xpath("//a[@href='/en/logout']")
        elif TEST_RESELLER == 'box-pn':
            self.driver.find_element_by_xpath("//a[@href='/logout']")
        else:
            pytest.fail('Unknown reseller in assert login test')
        return True

class AnonineLoginPage(object):
    def __init__(self, driver):
        self.driver = driver

    def login(self, username_or_email, password):
        self.enter_username_or_email(username_or_email)
        self.enter_password(password)
        client_area_page = self.submit_login()
        return client_area_page

    def can_not_login(self, username_or_email, password):
        self.enter_username_or_email(username_or_email)
        self.enter_password(password)
        self.submit_login()

    def open_reset_password_page(self):
        self.driver.find_element_by_css_selector("a[data-test='l-forgot-password']").click()
        reset_password_page = AnonineResetPasswordPage(self.driver)
        return reset_password_page

    def enter_username_or_email(self, username_or_email):
        username_or_email_element = self.driver.find_element_by_css_selector("input[data-test='l-username-input']")
        username_or_email_element.click()
        username_or_email_element.clear()
        username_or_email_element.send_keys(username_or_email)

    def enter_password(self, password):
        password_element = self.driver.find_element_by_css_selector("input[data-test='l-password-input']")
        password_element.click()
        password_element.clear()
        password_element.send_keys(password)

    def submit_login(self):
        self.driver.find_element_by_css_selector("button[data-test='l-submit']").click()
        return ClientAreaPage(self.driver)

    def exist_password_error(self):
        if TEST_RESELLER == 'anonine':
            self.driver.find_element_by_css_selector("div[data-test='l-filed-err-password']")
        else:
            pytest.fail('there is no sign in link')
        return True


class AnonineResetPasswordPage(object):
    def __init__(self, driver):
        self.driver = driver

    def send_reset_link(self, username_or_email):
        self.enter_username_or_email(username_or_email)
        self.submit_reset_password()

    def enter_username_or_email(self, username_or_email):
        username_or_email_element = self.driver.find_element_by_css_selector("input[data-test='fp-input-username']")
        username_or_email_element.click()
        username_or_email_element.clear()
        username_or_email_element.send_keys(username_or_email)

    def submit_reset_password(self):
        self.driver.find_element_by_css_selector("button[data-test='fp-submit']").click()

    def go_to_login_page(self):
        self.driver.find_element_by_css_selector("a[data-test='link-to-login']").click()

    def reset_link_is_sent_successfully(self):
        if self.driver.find_element_by_css_selector("div[data-test='fp-confirm-message']"):
            return True

    def incorrect_email_or_username(self):
        if self.driver.find_element_by_css_selector("div[data-test='fp-field-err-username']"):
            return True


class AnonineEnterNewPasswordPage(object):
    def __init__(self, driver):
        self.driver = driver

    def open(self, reset_link):
        script_open_window = "window.open('%s', 'new_window')" % reset_link
        self.driver.execute_script(script_open_window)
        self.driver.switch_to_window(self.driver.window_handles[1])

    def enter_and_confirm_new_password(self):
        self.enter_new_password()
        self.confirm_new_password()
        self.submit_new_password()
        self.driver.switch_to_window(self.driver.window_handles[0])

    def enter_new_password(self):
        new_password = self.driver.find_element_by_css_selector("input[data-test='up-password-input']")
        new_password.click()
        new_password.clear()
        new_password.send_keys(NEW_PASSWORD_FOR_RESET_PASSSWORD)

    def confirm_new_password(self):
        confirm_password = self.driver.find_element_by_css_selector("input[data-test='up-confirm-password-input']")
        confirm_password.click()
        confirm_password.clear()
        confirm_password.send_keys(NEW_PASSWORD_FOR_RESET_PASSSWORD)

    def submit_new_password(self):
        self.driver.find_element_by_css_selector("button[data-test='up-submit']").click()