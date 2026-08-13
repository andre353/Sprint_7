import requests
from endpoints.base_api import BaseApi
from urls import ENDPOINT_ORDERS


class OrdersApi(BaseApi):
    def create(self, payload):
        return requests.post(self._url(ENDPOINT_ORDERS), json=payload)

    def get_all(self):
        return requests.get(self._url(ENDPOINT_ORDERS))

    def accept(self, order_id=None, courier_id=None):
        params = {}
        if courier_id is not None:
            params["courierId"] = courier_id

        if order_id is None:
            return requests.put(self._url(f"{ENDPOINT_ORDERS}/accept"), params=params)

        return requests.put(self._url(f"{ENDPOINT_ORDERS}/accept/{order_id}"), params=params)

    def get_by_number(self, order_number=None):
        if order_number is None:
            return requests.get(self._url(f"{ENDPOINT_ORDERS}/track"))
        return requests.get(self._url(f"{ENDPOINT_ORDERS}/track"), params={"t": order_number})
        