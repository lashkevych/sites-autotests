import pytest
from selenium import webdriver

from site_autotest.settings import WAIT_TIMEOUT
from site_autotest.utils import create_user


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(WAIT_TIMEOUT)
    return selenium



@pytest.fixture
def with_driver(request, selenium):
    request.instance.driver = selenium

