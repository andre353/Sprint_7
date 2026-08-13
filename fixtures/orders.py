import pytest
from endpoints.orders_api import OrdersApi
from helpers import generate_order_payload
from urls import BASE_URL


@pytest.fixture(scope="session")
def orders_api():
    return OrdersApi(BASE_URL)


@pytest.fixture
def order_payload_black():
    return generate_order_payload(["BLACK"])


@pytest.fixture
def order_payload_grey():
    return generate_order_payload(["GREY"])


@pytest.fixture
def order_payload_both_colors():
    return generate_order_payload(["BLACK", "GREY"])


@pytest.fixture
def order_payload_no_color():
    return generate_order_payload()