from site_autotest.config import TEST_PASSWORD
from site_autotest.utils import set_text, generate_username
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class CompleteSignUpPage(object):
    def __init__(self, driver):
        self.driver = driver

    def complete_user_sign_up(self):
        from site_autotest.pages.client_area_page import ClientAreaPage
        self.enter_username()
        self.enter_and_confirm_password()
        self.submit_creds()
        return ClientAreaPage(self.driver)

    def submit_creds(self):
        self.driver.find_element_by_xpath("//button[@type='submit']").click()

    def enter_and_confirm_password(self):
        password = TEST_PASSWORD
        password_element = self.driver.find_element_by_id("new-password1")
        set_text(password_element, password)
        confirm_password_element = self.driver.find_element_by_id("new-password2")
        set_text(confirm_password_element, password)

    def enter_username(self):
        username = generate_username()
        username_element = self.driver.find_element_by_id("username")
        set_text(username_element, username)
