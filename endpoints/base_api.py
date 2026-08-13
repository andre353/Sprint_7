class BaseApi:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def _url(self, endpoint):
        return f"{self.base_url}/{endpoint.lstrip('/')}"