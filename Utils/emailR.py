import poplib
from email.header import decode_header
from bs4 import BeautifulSoup

from site_autotest.settings import SERVER

import email

class EmailServerWrapper(object):
    def __init__(self, user, password):
        # connect to server
        self.server = poplib.POP3_SSL(SERVER)

        # login
        self.server.user(user)
        self.server.pass_(password)

    def close_connect_to_email_server(self):
        self.server.quit()

    def confirm_email(self, email):
        pass

    def get_reset_link(self, user_email):
        # list items on server
        resp, items, octets = self.server.list()

        for i in range(0, len(items)):
            raw_message_string = self.get_raw_message(items[i])
            msg = email.message_from_string(raw_message_string)
            msg_subject = msg['subject']
            msg_to = msg['To']
            reset_password_subject = 'Anonine Password Reset Request'
            reset_password_link_text = 'RESET PASSWORD'
            #if (msg_subject.upper()==reset_password_subject.upper())& (msg_to==user_email):
            if (msg_subject.upper() == reset_password_subject.upper()):
                html_parts_list = self.parse(raw_message_string)
                for k in (0, len(html_parts_list)):
                    parsed_html_part = BeautifulSoup(html_parts_list[k])
                    for link in parsed_html_part.find_all('a'):
                        link_text = link.get_text()
                        if link_text.upper()==reset_password_link_text.upper():
                            return link.get('href')


    def readMail(self):
        # list items on server
        resp, items, octets = self.server.list()

        for i in range(0, 10):
            raw_message_string = self.get_raw_message(items[i])
            msg = email.message_from_string(raw_message_string)
            To = msg['To']
            Subject = msg['subject']

            html_parts_list = self.parse(raw_message_string)

            for k in (0, len(html_parts_list)):
                soup = BeautifulSoup(html_parts_list[k])
                for link in soup.find_all('a'):
                    link_text = link.get_text()
                    #VERIFY MY EMAIL ADDRESS

    def get_raw_message(self,raw_email):
        id, size = raw_email.split()
        resp, raw_message_lines_list, octets = self.server.retr(int(id))
        for j in range(0, len(raw_message_lines_list)):
            raw_message_lines_list[j] = raw_message_lines_list[j].decode("utf-8")

        raw_message_string = "\n".join(raw_message_lines_list)
        return  raw_message_string

    def parse(self, raw_message_text):
        message = email.message_from_string(raw_message_text)
        html_parts_list = []
        for i, part in enumerate(message.walk()):
            if part.get_content_type() == 'text/html':
                text = part.get_payload(decode=True)
                charset = part.get_param('charset', 'us-ascii')
                text = text.decode(charset)
                html_parts_list.append(text)
        return html_parts_list



