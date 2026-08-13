import pytest

from endpoints.courier_api import CourierApi
from helpers import generate_courier_payload, generate_login_payload
from urls import BASE_URL


@pytest.fixture(scope="session")
def courier_api():
    return CourierApi(BASE_URL)


@pytest.fixture
def courier_payload():
    return generate_courier_payload()


@pytest.fixture
def created_courier(courier_api, courier_payload):
    create_response = courier_api.create(courier_payload)
    courier_id = None

    if create_response.status_code == 201:
        login_response = courier_api.login(
            generate_login_payload(courier_payload["login"], courier_payload["password"])
        )
        if login_response.status_code in (200, 201):
            courier_id = login_response.json().get("id")

    yield courier_payload, courier_id

    if courier_id:
        courier_api.delete(courier_id)