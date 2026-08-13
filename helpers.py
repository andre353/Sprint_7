import random
import string
from datetime import datetime, timedelta


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = "".join(random.choice(letters) for _ in range(length))
    return random_string


def generate_courier_payload():
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10),
    }


def generate_login_payload(login=None, password=None):
    return {
        "login": login or generate_random_string(10),
        "password": password or generate_random_string(10),
    }


def generate_order_payload(colors=None):
    payload = {
        "firstName": "Test",
        "lastName": "User",
        "address": "Some street",
        "metroStation": 4,
        "phone": "+79990000000",
        "rentTime": 5,
        "deliveryDate": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "comment": "Test order",
    }
    if colors is not None:
        payload["color"] = colors
    return payload