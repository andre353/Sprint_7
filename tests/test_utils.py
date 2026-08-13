import allure
from helpers import generate_order_payload


@allure.epic("Яндекс.Самокат API")
@allure.feature("Служебные утилиты и поиск")
class TestUtils:
    @allure.story("Поиск заказов по номеру")
    @allure.title("Успешное получение полной информации о заказе по его трек-номеру")
    def test_get_order_by_number_success(self, orders_api):
        create_response = orders_api.create(generate_order_payload(["BLACK"]))
        assert create_response.status_code in (200, 201)
        track = create_response.json()["track"]

        response = orders_api.get_by_number(track)
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert "order" in response.json()

    def test_get_order_by_number_missing(self, orders_api):
        response = orders_api.get_by_number()
        assert response.status_code == 400
        assert response.json().get("message")

    def test_get_order_by_number_not_found(self, orders_api):
        response = orders_api.get_by_number(999999999)
        assert response.status_code in (400, 404)
        assert response.json().get("message")