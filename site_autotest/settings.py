import collections

from .config import *

HOSTNAMES = {
    'qa1': {
        'vpntunnel': "qa1-vpntunnel.vpnsvc.com",
        'box-pn': 'qa1-boxpn.vpnsvc.com',
        'anonine': 'qa1-anonine.vpnsvc.com'
    },
    'qa2': {
        'vpntunnel': "qa2-vpntunnel.vpnsvc.com",
        'box-pn': 'qa2-boxpn.vpnsvc.com',
        'anonine': 'qa2-anonine.vpnsvc.com'
    },
    'qa3': {
        'vpntunnel': "qa3-vpntunnel.vpnsvc.com",
        'box-pn': 'qa3-boxpn.vpnsvc.com',
        'anonine': 'qa3-anonine.vpnsvc.com'
    },
    'qa4': {
        'vpntunnel': "qa4-vpntunnel.vpnsvc.com",
        'box-pn': 'qa4-boxpn.vpnsvc.com',
        'anonine': 'qa4-anonine.vpnsvc.com'
    }
}

SERVER = "mail.vpnsvc.com"
HOSTNAME = HOSTNAMES[TEST_ENV][TEST_RESELLER]

#  for Chrome and Firefox
SITE_URL_WITH_BASIC_AUTH = "https://%s:%s@%s/" % (SITE_BASIC_AUTH_USERNAME, SITE_BASIC_AUTH_PASSWORD, HOSTNAME)

#  for Edge and IE
SITE_URL_NO_BASIC_AUTH = "https://%s/" % HOSTNAME

#params for reset password email parsing
SUBJECT_OF_RESET_PASSWORD_EMAIL = 'Anonine Password Reset Request'
LINK_TEXT_FOR_RESET_PASSWORD_EMAIL = 'RESET PASSWORD'

#params for confrim email parsing
SUBJECT_OF_CONFIRM_EMAIL_AFTER_PAYMENT = 'Thank you for your Interest in our Anonine Service!'
SUBJECT_OF_CONFIRM_EMAIL_AFTER_CHANGE_EMAIL = "Please Confirm your Email Address!"
LINK_TEXT_FOR_CONFIRM_EMAIL = 'VERIFY MY EMAIL ADDRESS'

# Implicit Waits
# seconds
WAIT_TIMEOUT = 30


# Explicit Waits
# seconds
DELAY_FOR_LOADING_PAGE = 60
DELAY_FOR_PAY_PAL_PAGE = 60

#DELAY_BEFORE_GETTING_EMAILS = 10
PAY_PAL_PAYMENT_REGISTRATION_TIMEOUT = 10

DELAY_BETWEEN_ATTEMPTS_OF_CHECKING_PAY_PAL_REGISTRATION = 5
MAXIMUM_ATTEMPTS_OF_CHECKING_PAY_PAL_REGISTRATION = 2

DELAY_BETWEEN_ATTEMPTS_OF_CHECKING_EMAIL = 5
MAXIMUM_ATTEMPTS_OF_CHECKING_EMAIL = 2

DELAY_BETWEEN_ATTEMPTS = 1

Card = collections.namedtuple('Card', 'number exp_month exp_year cvc_code zip_postal_code')

'''
CARDS = {
    'Visa_hypepay': Card(
        number='1234123412341234',
        exp_month='03', 
        exp_year='2019',
        cvc_code='111', 
        zip_postal_code='111111'),

    'MasterCards_hypepay': Card(
        number='5105105105105100',
        exp_month='03', 
        exp_year='19',
        cvc_code='111',
        zip_postal_code='111111'),

    'AmericanExpress_hypepay': Card(
        number='340000000000009',
        exp_month='03',
        exp_year='19',
        cvc_code='1111',
        zip_postal_code='111111')

}
'''