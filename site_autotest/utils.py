import collections
import random
import time

import pytest
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions



from site_autotest.settings import *


User = collections.namedtuple('User', 'username password email')


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

def unique_card_number_in_str(first_numeral_in_str):
    random.seed()
    str_time = str(unique_number())
    card_number = first_numeral_in_str + str_time
    for i in range(1, 16 - len(str_time)):
        num = random.randint(0, 9)
        card_number = card_number + str(num)
    return card_number

def generate_username():
    return "test_user_%s" % unique_number()

def generate_email(email_prefix):
    email = USER_EMAIL_TEMPLATE % (email_prefix, unique_number())
    return email

def generate_card_number(card_type):
    if card_type == 'Visa_hypepay':
        card_number = unique_card_number_in_str('4')
    elif card_type == 'MasterCards_hypepay':
        card_number = unique_card_number_in_str('5')
    elif card_type ==  'AmericanExpress_hypepay':
        card_number = unique_card_number_in_str('3')
    else:
        pytest.fail('unknown card type in generate card number')
    return  card_number

def generate_random_card(card_type):
    if card_type == 'Visa_hypepay':
        random_card = Card(
            number=generate_card_number(card_type),
            exp_month='03',
            exp_year='2019',
            cvc_code='111',
            zip_postal_code='111111')
    elif card_type == 'MasterCards_hypepay':
        random_card = Card(
            number=generate_card_number(card_type),
            exp_month='03',
            exp_year='19',
            cvc_code='111',
            zip_postal_code='111111')
    elif card_type ==  'AmericanExpress_hypepay':
        random_card = Card(
            number=generate_card_number(card_type),
            exp_month='03',
            exp_year='19',
            cvc_code='1111',
            zip_postal_code='111111')
    else:
        pytest.fail('unknown card type in generate random card')
    return random_card

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

def wait_for(driver, time, method_for_executing, message, wait_until=True):
    try:
        if wait_until:
            WebDriverWait(driver, time).until(method_for_executing)
        else:
            WebDriverWait(driver,time).until_not(method_for_executing)
    except TimeoutException:
        pytest.fail(message)

def  click_with_waiting_page_reload(method):
    max_waiting_time_sec = time.time()+ DELAY_FOR_LOADING_PAGE
    while True:
        try:
            elem = method()
            elem.click()
            break
        except StaleElementReferenceException:
            if time.time()>= max_waiting_time_sec:
                raise
            time.sleep(10)
