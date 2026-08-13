import requests
from endpoints.base_api import BaseApi
from urls import ENDPOINT_COURIER


class CourierApi(BaseApi):
    def create(self, payload):
        return requests.post(self._url(ENDPOINT_COURIER), json=payload)

    def login(self, payload):
        return requests.post(self._url(f"{ENDPOINT_COURIER}/login"), json=payload)

    def delete(self, courier_id=None):
        if courier_id is None:
            return requests.delete(self._url(ENDPOINT_COURIER))
        return requests.delete(self._url(f"{ENDPOINT_COURIER}/{courier_id}"))