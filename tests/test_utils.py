import allure
from helpers import generate_order_payload
from data import get_base_order_data


@allure.epic("Яндекс.Самокат API")
@allure.feature("Служебные утилиты и поиск")
class TestUtils:
    @allure.story("Поиск заказов по номеру")
    @allure.title("Успешное получение полной информации о заказе по его трек-номеру")
    def test_get_order_by_number_success(self, orders_api):
        base_data = get_base_order_data()
        create_response = orders_api.create(generate_order_payload(base_data, ["BLACK"]))
        track = create_response.json()["track"]

        response = orders_api.get_by_number(track)
        assert (response.status_code == 200 and 
                isinstance(response.json(), dict) and 
                "order" in response.json())

    @allure.story("Поиск заказов по номеру")
    @allure.title("Ошибка при запросе без номера заказа")
    def test_get_order_by_number_missing(self, orders_api):
        response = orders_api.get_by_number()
        assert response.status_code == 400 and response.json().get("message")

    @allure.story("Поиск заказов по номеру")
    @allure.title("Ошибка при поиске несуществующего трек-номера")
    def test_get_order_by_number_not_found(self, orders_api):
        response = orders_api.get_by_number(999999999)
        assert response.status_code in (400, 404) and response.json().get("message")