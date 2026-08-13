import pytest
from helpers import generate_order_payload


class TestOrders:
    @pytest.mark.parametrize(
        "payload",
        [
            generate_order_payload(["BLACK"]),
            generate_order_payload(["GREY"]),
            generate_order_payload(["BLACK", "GREY"]),
            generate_order_payload(),
        ],
    )
    def test_create_order_success(self, orders_api, payload):
        response = orders_api.create(payload)
        assert response.status_code in (200, 201)
        assert "track" in response.json()

    def test_get_orders_list(self, orders_api):
        response = orders_api.get_all()
        orders_data = response.json().get("orders")
        assert (response.status_code == 200 and 
            isinstance(orders_data, list) and 
            len(orders_data) > 0)

    def test_accept_order_success(self, orders_api, created_courier):
        _, courier_id = created_courier

        if courier_id is None:
            assert False, "Courier was not created for test setup"

        order_response = orders_api.create(generate_order_payload(["BLACK"]))
        assert order_response.status_code in (200, 201)
        track = order_response.json()["track"]

        order_info = orders_api.get_by_number(track)
        assert order_info.status_code == 200
        order_id = order_info.json()["order"]["id"]

        accept_response = orders_api.accept(order_id=order_id, courier_id=courier_id)
        assert accept_response.status_code == 200
        assert accept_response.json() == {"ok": True}

    def test_accept_order_without_courier_id(self, orders_api):
        response = orders_api.accept(order_id=1)
        assert response.status_code in (400, 404)
        assert response.json().get("message")

    def test_accept_order_with_wrong_courier_id(self, orders_api):
        response = orders_api.accept(order_id=1, courier_id=999999999)
        assert response.status_code in (400, 404)
        assert response.json().get("message")

    def test_accept_order_without_order_id(self, orders_api):
        response = orders_api.accept(courier_id=1)
        assert response.status_code in (400, 404)
        assert response.json().get("message")

    def test_accept_order_with_wrong_order_id(self, orders_api):
        response = orders_api.accept(order_id=999999999, courier_id=1)
        assert response.status_code in (400, 404)
        assert response.json().get("message")