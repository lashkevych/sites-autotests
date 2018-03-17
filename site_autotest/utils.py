import time


def send_keys_slowly(element, text):
    for c in text:
        element.send_keys(c)
        time.sleep(0.1)


def set_text(element, text):
    element.click()
    element.clear()
    send_keys_slowly(element, text)