import allure
import pytest
from helpers import generate_order_payload
from data import get_base_order_data

@allure.epic("Яндекс.Самокат API")
@allure.feature("Управление заказами")
class TestOrders:

    @allure.story("Создание заказов")
    @allure.title("Параметризованный тест создания заказа с выбором различных цветов")
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ])
    def test_create_order_success(self, orders_api, colors):
        # 1. Генерируем уникальный набор базовых данных для теста
        base_data = get_base_order_data()
        
        # 2. Передаем свежие данные и цвет в хелпер для сборки финального payload
        payload = generate_order_payload(base_data, colors)        
        response = orders_api.create(payload)        
        assert response.status_code in (200, 201) and "track" in response.json()

    @allure.story("Получение информации о заказах")
    @allure.title("Получение общего списка всех существующих заказов")
    def test_get_orders_list(self, orders_api):
        response = orders_api.get_all()
        orders_data = response.json().get("orders")
        assert (response.status_code == 200 and 
            isinstance(orders_data, list) and 
            len(orders_data) > 0)

    @allure.story("Принятие заказа курьером")
    @allure.title("Успешное принятие существующего заказа валидным курьером")
    def test_accept_order_success(self, orders_api, created_courier):
        _, courier_id = created_courier

        if courier_id is None:
            assert False, "Courier was not created for test setup"

        base_data = get_base_order_data()
        order_response = orders_api.create(generate_order_payload(base_data, ["BLACK"]))
        track = order_response.json()["track"]
        
        order_info = orders_api.get_by_number(track)
        order_id = order_info.json()["order"]["id"]
        
        accept_response = orders_api.accept(order_id=order_id, courier_id=courier_id)
        
        assert (order_info.status_code == 200 and 
                accept_response.status_code == 200 and 
                accept_response.json() == {"ok": True})

    @allure.story("Принятие заказа курьером")
    @allure.title("Ошибка при принятии заказа без указания ID курьера")
    def test_accept_order_without_courier_id(self, orders_api):
        response = orders_api.accept(order_id=1)
        
        assert response.status_code in (400, 404) and response.json().get("message")

    @allure.story("Принятие заказа курьером")
    @allure.title("Ошибка при принятии заказа несуществующим курьером")
    def test_accept_order_with_wrong_courier_id(self, orders_api):
        response = orders_api.accept(order_id=1, courier_id=999999999)
        
        assert response.status_code in (400, 404) and response.json().get("message")

    @allure.story("Принятие заказа курьером")
    @allure.title("Ошибка при принятии заказа без указания ID заказа")
    def test_accept_order_without_order_id(self, orders_api):
        response = orders_api.accept(courier_id=1)
        
        assert response.status_code in (400, 404) and response.json().get("message")

    @allure.story("Принятие заказа курьером")
    @allure.title("Ошибка при принятии несуществующего заказа")
    def test_accept_order_with_wrong_order_id(self, orders_api):
        response = orders_api.accept(order_id=999999999, courier_id=1)

        assert response.status_code in (400, 404) and response.json().get("message")