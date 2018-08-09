import collections

from .config import *

HOSTNAMES = {
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
SITE_URL_CHROME_FIREFOX = "https://%s:%s@%s/" % (SITE_BASIC_AUTH_USERNAME, SITE_BASIC_AUTH_PASSWORD, HOSTNAME)
WAIT_TIMEOUT = 30
DELAY_BETWEEN_ATTEMPTS = 1

Card = collections.namedtuple('Card', 'number exp_month exp_year cvc_code zip_postal_code')

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