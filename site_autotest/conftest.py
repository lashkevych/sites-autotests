import pytest
from selenium import webdriver

from site_autotest.settings import WAIT_TIMEOUT
from site_autotest.utils import create_user

from selenium import webdriver

@pytest.fixture
def driver_fixture(selenium):
    selenium.implicitly_wait(WAIT_TIMEOUT)
    return selenium

#def driver_fixture():
#    return webdriver.Ie()