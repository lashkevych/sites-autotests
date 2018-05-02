import collections

from .config import *

HOSTNAMES = {
    'qa2': {
        'vpntunnel': "qa2-vpntunnel.vpnsvc.com"
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
        number='4532-7597-3454-5858', 
        exp_month='03', 
        exp_year='2019',
        cvc_code='111', 
        zip_postal_code='111111'),

    'MasterCards_squareup': Card(
        number='5409-8899-4417-9029', 
        exp_month='03', 
        exp_year='2019',
        cvc_code='111',
        zip_postal_code='111111'),

    'AmericanExpress_squareup': Card(
        number='3712-6346-2726-550',
        exp_month='03',
        exp_year='2019',
        cvc_code='1111',
        zip_postal_code='111111'),

    'Visa_squareup_incorrect_cvc': Card(
        #number='4532-7597-3454-5858',
        number='4242-4242-4242-4242',
        exp_month='03',
        exp_year='2019',
        cvc_code='911',
        zip_postal_code='111111'),

    'Visa_squareup_incorrect_zip': Card(
        #number='4532-7597-3454-5858',
        number='4242-4242-4242-4242',
        exp_month='03',
        exp_year='2019',
        cvc_code='111',
        zip_postal_code='99999'),

    'Visa_squareup_incorrect_exp_date': Card(
        #number='4532-7597-3454-5858',
        number='4242-4242-4242-4242',
        exp_month='01',
        exp_year='2036',
        #exp_year='40'
        cvc_code='111',
        zip_postal_code='111111')
}