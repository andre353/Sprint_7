import random
from helpers import generate_random_string
from datetime import datetime, timedelta

def get_base_order_data():
    """Возвращает новый словарь с уникальными случайными данными при каждом вызове"""
    return {
        "firstName": f"Имя_{generate_random_string(5)}",
        "lastName": f"Фам_{generate_random_string(5)}",
        "address": f"Улица {generate_random_string(8)}, д. 10",
        "metroStation": random.randint(1, 10),
        "phone": f"+7999{random.randint(1000000, 9999999)}",
        "rentTime": random.randint(1, 5),
        "deliveryDate": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "comment": "Тестовый комментарий к заказу",
    }

# Идентификаторы для негативных тест-кейсов (несуществующие сущности)
NON_EXISTENT_ID = 999999999
MOCK_TEST_ID = 1