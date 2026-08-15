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


def generate_order_payload(base_data, colors=None):
    # Делаем копию, чтобы не изменять оригинальный словарь в data.py
    payload = base_data.copy()
    if colors is not None:
        payload["color"] = colors
    return payload