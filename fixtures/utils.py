import pytest

from endpoints.utils_api import UtilsApi
from urls import BASE_URL


@pytest.fixture(scope="session")
def utils_api():
    return UtilsApi(BASE_URL)