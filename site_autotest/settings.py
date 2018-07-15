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
HOSTNAME = HOSTNAMES[TEST_ENV][TEST_RESELLER]
SITE_URL = "https://%s:%s@%s/" % (SITE_BASIC_AUTH_USERNAME, SITE_BASIC_AUTH_PASSWORD, HOSTNAME)
WAIT_TIMEOUT = 30
DELAY_BETWEEN_ATTEMPTS = 1

Card = collections.namedtuple('Card', 'number exp_month exp_year cvc_code zip_postal_code')

CARDS = {
    'Visa_stripe': Card(
        number='4242-4242-4242-4242', 
        exp_month='03', 
        exp_year='2019',
        cvc_code='111', 
        zip_postal_code='111111'),

    'Visa_squareup': Card(
        number='4111111111111111',
        exp_month='12',
        exp_year='20',
        cvc_code='111', 
        zip_postal_code='111111'),

    'MasterCards_squareup': Card(
        number='5105105105105100',
        exp_month='03', 
        exp_year='19',
        cvc_code='111',
        zip_postal_code='111111'),

    'AmericanExpress_squareup': Card(
        number='340000000000009',
        exp_month='03',
        exp_year='19',
        cvc_code='1111',
        zip_postal_code='111111'),

    'Visa_squareup_incorrect_cvc': Card(
        number='4111111111111111',
        exp_month='03',
        exp_year='19',
        cvc_code='911',
        zip_postal_code='111111'),

    'Visa_squareup_incorrect_zip': Card(
        number='4111111111111111',
        exp_month='03',
        exp_year='19',
        cvc_code='111',
        zip_postal_code='99999'),

    'Visa_squareup_incorrect_exp_date': Card(
        number='4111111111111111',
        exp_month='01',
        exp_year='40',
        #exp_year='40'
        cvc_code='111',
        zip_postal_code='111111')
}