

class ControlPanel(object):
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.find_element_by_link_text('CONTROL PANEL').click()

    def go_to_upgrade_page(self):
        self.driver.find_element_by_partial_link_text('UPGRADE').click()



