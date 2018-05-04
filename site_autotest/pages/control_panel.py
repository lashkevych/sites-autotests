from time import sleep

from site_autotest.pages.payment import PaymentPage
from site_autotest.settings import DELAY_BETWEEN_ATTEMPTS


class ControlPanelPage(object):
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.find_element_by_link_text('CONTROL PANEL').click()

    def open_upgrade_page(self):
        self.driver.find_element_by_partial_link_text('UPGRADE').click()
        sleep(DELAY_BETWEEN_ATTEMPTS+1)
        return PaymentPage(self.driver)

    def exist_logout_link(self):
        try:
            self.driver.find_element_by_xpath("//a[@href='/en/logout']")
            return True
        except:
            return False




