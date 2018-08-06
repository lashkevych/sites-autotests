from time import sleep

from site_autotest.settings import DELAY_BETWEEN_ATTEMPTS


class ProfilePage(object):
    def __init__(self, driver):
        self.driver = driver

    def get_last_plan(self):
        return self.driver.find_element_by_xpath("//table[@class = 'table-history-body']/tbody/tr[1]/td[2]").text

    def exist_subscription(self):
        if self.driver.find_element_by_xpath("//a[@id='cancel_inovio_subscription']"):
            return True
        else:
            return False

    def user_is_no_creds(self):
        if self.driver.find_element_by_xpath("//input[@id='username']"):
            return True
        else:
            return False

class ControlPanelPage(object):
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.find_element_by_link_text('CONTROL PANEL').click()

    #ACCOUNT

    def open_payment_page(self):
        from site_autotest.pages.payment import PaymentPage
        self.driver.find_element_by_partial_link_text('UPGRADE').click()
        sleep(DELAY_BETWEEN_ATTEMPTS+1)
        return PaymentPage(self.driver)

    def open_profile_page(self):
        #self.driver.find_element_by_partial_link_text('PROFILE').click()
        el = self.driver.find_element_by_class_name('dashboard-content')
        el.find_element_by_partial_link_text('PROFILE').click()

        sleep(DELAY_BETWEEN_ATTEMPTS+1)
        return ProfilePage(self.driver)

    def open_profile_page_no_creds_user(self):
        el = self.driver.find_element_by_xpath("//a//div[text()='Profile']")
        el = el.find_element_by_xpath('..')
        el.click()

        sleep(DELAY_BETWEEN_ATTEMPTS+1)
        return ProfilePage(self.driver)

    def exist_logout_link(self):
        try:
            self.driver.find_element_by_xpath("//a[@href='/en/logout']")
            return True
        except:
            return False




