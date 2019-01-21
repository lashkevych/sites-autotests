from site_autotest.config import TEST_PASSWORD
from site_autotest.utils import set_text, generate_user

class CompleteSignUpPage(object):
    def __init__(self, driver):
        self.driver = driver

    def complete_user_sign_up(self, user=None):
        from site_autotest.pages.client_area_page import ClientAreaPage
        if user:
            user_data = user
        else:
            user_data = generate_user()
        self.enter_username(user_data.username)
        self.enter_and_confirm_password(user_data.password)
        self.submit_creds()
        return ClientAreaPage(self.driver)

    def submit_creds(self):
        self.driver.find_element_by_xpath("//button[@type='submit']").click()

    def enter_and_confirm_password(self,password):
        password_element = self.driver.find_element_by_id("new-password1")
        set_text(password_element, password)
        confirm_password_element = self.driver.find_element_by_id("new-password2")
        set_text(confirm_password_element, password)

    def enter_username(self, username):
        username_element = self.driver.find_element_by_id("username")
        set_text(username_element, username)
