
from site_autotest.pages.payment import PaymentPage

class ControlPanelPage(object):
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.find_element_by_link_text('CONTROL PANEL').click()

    def open_upgrade_page(self):
        self.driver.find_element_by_partial_link_text('UPGRADE').click()
        return PaymentPage(self.driver)

    def exist_logout_link(self):
        try:
            self.driver.find_element_by_xpath("//a[@href='/en/logout']")
            return True
        except:
            return False



