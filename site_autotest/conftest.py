import pytest

from site_autotest.settings import WAIT_TIMEOUT


@pytest.fixture
def driver_fixture(selenium, variables):
    selenium.implicitly_wait(WAIT_TIMEOUT)
    return selenium


@pytest.fixture
def driver_kwargs(driver_kwargs, variables):
    if 'driver_kwargs' in variables:
        if driver_kwargs:
            driver_kwargs.update(variables['driver_kwargs'])
        else:
            driver_kwargs = variables['driver_kwargs']
    return driver_kwargs