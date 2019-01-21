import pytest

from site_autotest.config import TEST_RESELLER

class AnonineContactPage(object):
    def __init__(self, driver):
        self.driver = driver

    def send_message_to_support(self, email, subject, message):
        self.enter_email(email)
        self.enter_subject(subject)
        self.enter_message(message)
        message_sent_page = self.submit_send_message()
        return message_sent_page

    def enter_email(self, email):
        email_element = self.driver.find_element_by_css_selector("input[data-test='email']")
        email_element.click()
        email_element.clear()
        email_element.send_keys(email)

    def enter_subject(self, subject):
        subject_element = self.driver.find_element_by_css_selector("input[data-test='subject']")
        subject_element.click()
        subject_element.clear()
        subject_element.send_keys(subject)

    def enter_message(self, message):
        message_element = self.driver.find_element_by_css_selector("textarea[data-test='message']")
        message_element.click()
        message_element.clear()
        message_element.send_keys(message)

    def submit_send_message(self):
        self.driver.find_element_by_css_selector("button[data-test='send-button']").click()
        return MessageSentPage(self.driver)


class MessageSentPage(object):
    def __init__(self, driver):
        self.driver = driver

    def exist_success_message(self):
        if TEST_RESELLER == 'anonine':
            self.driver.find_element_by_css_selector("div[data-test='message-successful-submit']")
        else:
            pytest.fail('there is no success message about sending message to support')
        return True
