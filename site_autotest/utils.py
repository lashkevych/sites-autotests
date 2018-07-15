import collections
import time

import pytest
import requests


from site_autotest.config import *
from site_autotest.settings import HOSTNAME


def send_keys_slowly(element, text):
    for c in text:
        element.send_keys(c)
        time.sleep(0.1)

def set_text(element, text):
    element.click()
    element.clear()
    send_keys_slowly(element, text)

def unique_number():
    return int(1000 * time.time())

def generate_username():
    return "test_user_%s" % unique_number()

def generate_email(email_prefix):
    email = USER_EMAIL_TEMPLATE % (email_prefix, unique_number())
    return email


User = collections.namedtuple('User', 'username password email')


def create_user(email_prefix=''):
    user = User(username=generate_username(), password=TEST_PASSWORD, email=generate_email(email_prefix))
    params = {'username': user.username, 'email': user.email, 'password':user.password,
              'passconfirm':user.password, 'emailconfirm':user.email, 'agree':'1'}
    if TEST_RESELLER == 'anonine':
        r = requests.post("http://%s/en/ajax/register-user" % HOSTNAME,
                          auth=(SITE_BASIC_AUTH_USERNAME, SITE_BASIC_AUTH_PASSWORD), data=params)
    elif TEST_RESELLER == 'box-pn':
        r = requests.post("http://%s/ajax/register-user" % HOSTNAME,
                          auth=(SITE_BASIC_AUTH_USERNAME, SITE_BASIC_AUTH_PASSWORD), data=params)
    else:
        pytest.fail('unknown reseller in create user')
    #assert r.ok, r.text
    return user
