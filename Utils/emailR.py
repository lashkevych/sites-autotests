import poplib
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from site_autotest.settings import SERVER

import email

class AnonineEmailClientWrapper(object):
    def __init__(self, user, password):
        # connect to server
        self.server = poplib.POP3_SSL(SERVER)

        # login
        self.server.user(user)
        self.server.pass_(password)

    def close_connect_to_email_server(self):
        self.server.quit()

    def get_link(self, user_email, subject, link_text):
        resp, items, octets = self.server.list()
        for i in reversed(range(0, len(items))):
            raw_message_string = self.get_raw_message(items[i])
            msg = email.message_from_string(raw_message_string)
            msg_subject = msg['subject']
            #msg_date = datetime.strptime(msg['Date'], '%a, %d %b %Y %H:%M:%S %z')
            #datetime.now() - timedelta(days=1)
            msg_to = msg['To']
            if (msg_subject.upper()==subject.upper())& (msg_to==user_email):
                html_parts_list = self.parse(raw_message_string)
                for k in (0, len(html_parts_list)):
                    parsed_html_part = BeautifulSoup(html_parts_list[k])
                    for link in parsed_html_part.find_all('a'):
                        msg_link_text = link.get_text()
                        if msg_link_text.upper()==link_text.upper():
                            return link.get('href')
        return None

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




