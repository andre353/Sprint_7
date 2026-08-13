class TestCourier:
    def test_create_courier_success(self, courier_api, courier_payload):
        response = courier_api.create(courier_payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

        login_response = courier_api.login(
            {"login": courier_payload["login"], "password": courier_payload["password"]}
        )
        assert login_response.status_code in (200, 201)
        assert "id" in login_response.json()

        courier_id = login_response.json()["id"]
        delete_response = courier_api.delete(courier_id)
        assert delete_response.status_code in (200, 202, 204)
        assert delete_response.json() == {"ok": True}

    def test_create_duplicate_courier(self, courier_api, courier_payload):
        first = courier_api.create(courier_payload)
        assert first.status_code == 201

        second = courier_api.create(courier_payload)
        assert second.status_code in (400, 409)
        assert second.json().get("message")

        login_response = courier_api.login(
            {"login": courier_payload["login"], "password": courier_payload["password"]}
        )
        if login_response.status_code in (200, 201):
            courier_id = login_response.json()["id"]
            courier_api.delete(courier_id)

    def test_create_courier_without_login(self, courier_api):
        response = courier_api.create({"password": "pass123", "firstName": "Name"})
        assert response.status_code == 400
        assert response.json().get("message")

    def test_create_courier_without_password(self, courier_api):
        response = courier_api.create({"login": "login123", "firstName": "Name"})
        assert response.status_code == 400
        assert response.json().get("message")

    def test_login_courier_success(self, courier_api, created_courier):
        payload, _ = created_courier
        create_response = courier_api.create(payload)
        if create_response.status_code == 201:
            response = courier_api.login({"login": payload["login"], "password": payload["password"]})
            assert response.status_code in (200, 201)
            assert "id" in response.json()
            courier_id = response.json()["id"]
            courier_api.delete(courier_id)

    def test_login_missing_login(self, courier_api):
        response = courier_api.login({"password": "password123"})
        assert response.status_code == 400
        assert response.json().get("message")

    def test_login_missing_password(self, courier_api):
        response = courier_api.login({"login": "login123", "password": ""})
        assert response.status_code == 400
        assert response.json().get("message")

    def test_login_wrong_login(self, courier_api):
        response = courier_api.login({"login": "wrong_login", "password": "password123"})
        assert response.status_code == 404
        assert response.json().get("message")

    def test_login_wrong_password(self, courier_api, created_courier):
        payload, _ = created_courier
        response = courier_api.login({"login": payload["login"], "password": "wrong_password"})
        assert response.status_code in (400, 404)
        assert response.json().get("message")

    def test_delete_courier_without_id(self, courier_api):
        response = courier_api.delete()
        assert response.status_code in (400, 404)
        assert response.json().get("message")

    def test_delete_courier_not_found(self, courier_api):
        response = courier_api.delete(999999999)
        assert response.status_code in (400, 404)
        assert response.json().get("message")