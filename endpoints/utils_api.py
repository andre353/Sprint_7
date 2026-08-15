import requests
from endpoints.base_api import BaseApi
from urls import ENDPOINT_UTILS


class UtilsApi(BaseApi):
    def get_all(self):
        return requests.get(self._url(ENDPOINT_UTILS))
        