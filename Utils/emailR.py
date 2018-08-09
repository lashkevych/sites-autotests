import poplib
import string

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

    def readMail(self):
        # list items on server
        resp, items, octets = self.server.list()

        for i in range(0, 10):
            id, size = items[i].split()
            resp, raw_message_lines_list, octets = self.server.retr(int(id))
            for j in range(0,len(raw_message_lines_list)):
                raw_message_lines_list[j] = raw_message_lines_list[j].decode("utf-8")

            raw_message_string = "\n".join(raw_message_lines_list)

            html_parts_list = self.parse(raw_message_string)

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



