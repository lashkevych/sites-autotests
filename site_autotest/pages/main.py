import time

import pytest

from site_autotest.config import *
from site_autotest.settings import SITE_URL_WITH_BASIC_AUTH, SITE_URL_NO_BASIC_AUTH, \
    DELAY_BETWEEN_ATTEMPTS, DELAY_FOR_LOADING_PAGE
from site_autotest.pages.control_panel import ControlPanelPage
from site_autotest.pages.payment import PaymentPage
from Utils.emailR import EmailServerWrapper


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
            self.driver.find_element_by_css_selector("a[data-test='buy']").click()
        else:
            pytest.fail('unknown reseller in open order page')
        return PaymentPage(self.driver)

    def open_client_area_page(self):
        if TEST_RESELLER == 'anonine':
            self.driver.find_element_by_link_text('ACCOUNT').click()
        else:
            pytest.fail('unknown reseller in open order page')
        return ControlPanelPage(self.driver)

    def get_login_form(self):
        return LOGIN_FORMS[TEST_RESELLER](self.driver)

    def get_new_password_form(self):
        return NEW_PASSWORD_FORMS[TEST_RESELLER](self.driver)

    def exist_logout_link(self):
        if TEST_RESELLER == 'anonine':
            self.driver.find_element_by_xpath("//a[@href='/en/logout']")
        elif TEST_RESELLER == 'box-pn':
            self.driver.find_element_by_xpath("//a[@href='/logout']")
        else:
            pytest.fail('unknown reseller in assert login test')
        return True

class AnonineLoginForm(object):
    def __init__(self, driver):
        self.driver = driver

    def login(self, username_or_email, password):
        self.enter_username_or_email(username_or_email)
        self.enter_password(password)
        return self.submit_login()

    def login_after_logout(self,username_or_email,password):
        self.logout()
        self.open_login_form()
        self.enter_username_or_email(username_or_email)
        self.enter_password(password)
        return self.submit_login()

    def logout(self):
        self.driver.find_element_by_xpath("//a[@href='/en/logout'][@class='auth-logo']").click()
        time.sleep(DELAY_FOR_LOADING_PAGE)

    def open_login_form(self):
        self.driver.find_element_by_css_selector("a[data-test='sign-in']").click()
        time.sleep(DELAY_FOR_LOADING_PAGE)

    def open_reset_form(self):
        self.driver.find_element_by_css_selector("a[data-test='l-forgot-password']").click()
        time.sleep(DELAY_FOR_LOADING_PAGE)
        return RESET_PASSWORD_FORMS[TEST_RESELLER](self.driver)

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
        return ControlPanelPage(self.driver)


class BoxpnLoginForm(object):
    def __init__(self, driver):
        self.driver = driver

    def login(self, username_or_email, password):
        self.open_login_form()
        self.enter_username_or_email(username_or_email)
        self.enter_password(password)
        return self.submit_login()

    def open_login_form(self):
        #method is necessary for working the same way as Anonine LoginForm
        time.sleep(DELAY_BETWEEN_ATTEMPTS)

    def login_after_logout(self, username_or_email, password):
        self.logout()
        self.enter_username_or_email(username_or_email)
        self.enter_password(password)
        return self.submit_login()

    def logout(self):
        self.driver.find_element_by_xpath("//a[@href='/logout'][@class='auth-logo']").click()
        time.sleep(DELAY_BETWEEN_ATTEMPTS)

    def enter_username_or_email(self, username_or_email):
        username_or_email_element = self.driver.find_element_by_css_selector("input[name='username_or_email']")
        username_or_email_element.click()
        username_or_email_element.clear()
        username_or_email_element.send_keys(username_or_email)

    def enter_password(self, password):
        password_element = self.driver.find_element_by_css_selector("input[name='password']")
        password_element.click()
        password_element.clear()
        password_element.send_keys(password)

    def submit_login(self):
        self.driver.find_element_by_xpath("//form[@id='loginForm']//button[@type='submit']").click()
        return ControlPanelPage(self.driver)

    def open_reset_form(self):
        self.driver.find_element_by_link_text("Forgot password").click()
        time.sleep(DELAY_BETWEEN_ATTEMPTS)
        return RESET_PASSWORD_FORMS[TEST_RESELLER](self.driver)


class AnonineResetPasswordForm(object):
    def __init__(self, driver):
        self.driver = driver

    def send_reset_link(self, username_or_email):
        self.enter_username_or_email(username_or_email)
        self.submit_reset_password()
        return self.reset_link_is_sent_successfully()

    def enter_username_or_email(self, username_or_email):
        username_or_email_element = self.driver.find_element_by_css_selector("input[data-test='fp-input-username']")
        username_or_email_element.click()
        username_or_email_element.clear()
        username_or_email_element.send_keys(username_or_email)

    def submit_reset_password(self):
        self.driver.find_element_by_css_selector("button[data-test='fp-submit']").click()

    def go_to_login_form(self):
        self.driver.find_element_by_css_selector("a[data-test='link-to-login']").click()

    def reset_link_is_sent_successfully(self):
        if self.driver.find_element_by_css_selector("div[data-test='fp-confirm-message']"):
            return True
        else:
            return False


class BoxpnResetPasswordForm(object):
    def __init__(self, driver):
        self.driver = driver

    def send_reset_link(self, username_or_email):
        self.enter_username_or_email(username_or_email)
        self.submit_reset_password()
        return self.reset_link_is_sent_successfully()

    def enter_username_or_email(self, username_or_email):
        username_or_email_element = self.driver.find_element_by_xpath("//input[@name='username_or_email']")
        username_or_email_element.click()
        username_or_email_element.clear()
        username_or_email_element.send_keys(username_or_email)

    def submit_reset_password(self):
        self.driver.find_element_by_xpath("//form[@id='resetPasswordForm']//button[@id='resetPasswordButton']").click()

    def reset_link_is_sent_successfully(self):
        if self.driver.find_element_by_xpath("//*[text()='Check your e-mail to reset your password']"):
            return True
        else:
            return False

class AnonineEnterNewPasswordForm(object):
    def __init__(self, driver):
        self.driver = driver

    def open(self, user_email):
        email_server_wrapper = EmailServerWrapper(QA_EMAIL, QA_EMAIL_PASSWORD)
        reset_link = email_server_wrapper.get_reset_link(user_email)
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


class BoxpnEnterNewPasswordForm(object):
    def __init__(self, driver):
        self.driver = driver

    def open(self, user_email):
        email_server_wrapper = EmailServerWrapper(QA_EMAIL, QA_EMAIL_PASSWORD)
        # reset_link = email_server_wrapper.get_reset_link(QA_EMAIL)
        reset_link = email_server_wrapper.get_reset_link(user_email)
        script_open_window = "window.open('%s', 'new_window')" % reset_link
        self.driver.execute_script(script_open_window)
        self.driver.switch_to_window(self.driver.window_handles[1])

    def enter_and_confirm_new_password(self):
        self.enter_new_password()
        self.confirm_new_password()
        self.submit_new_password()
        self.driver.switch_to_window(self.driver.window_handles[0])

    def enter_new_password(self):
        new_password = self.driver.find_element_by_id("password")
        new_password.click()
        new_password.clear()
        new_password.send_keys(NEW_PASSWORD_FOR_RESET_PASSSWORD)

    def confirm_new_password(self):
        confirm_password = self.driver.find_element_by_id("passconfirm")
        confirm_password.click()
        confirm_password.clear()
        confirm_password.send_keys(NEW_PASSWORD_FOR_RESET_PASSSWORD)

    def submit_new_password(self):
        self.driver.find_element_by_xpath("//form[@class='login_form']//button[@type='submit']").click()




LOGIN_FORMS = {
    'anonine': AnonineLoginForm,
    'box-pn': BoxpnLoginForm,
}

RESET_PASSWORD_FORMS = {
    'anonine': AnonineResetPasswordForm,
    'box-pn': BoxpnResetPasswordForm,
}

NEW_PASSWORD_FORMS = {
    'anonine': AnonineEnterNewPasswordForm,
    'box-pn': BoxpnEnterNewPasswordForm,
}