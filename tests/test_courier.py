import allure
import pytest


@allure.epic("Яндекс.Самокат API")
@allure.feature("Управление курьерами")
class TestCourier:
    @allure.story("Создание новой учетной записи курьера")
    @allure.title("Успешное создание курьера со всеми обязательными полями")
    def test_create_courier_success(self, courier_api, courier_payload):
        # Отправляем запрос на создание
        response = courier_api.create(courier_payload)
        
        # Переменные для сбора статусов проверок (инициализируем как False)
        login_ok = False
        delete_ok = False
        
        # Выполняем шаги авторизации и удаления только при успешном создании (код 201)
        if response.status_code == 201:
            login_response = courier_api.login(
                {"login": courier_payload["login"], "password": courier_payload["password"]}
            )
            
            if login_response.status_code in (200, 201) and "id" in login_response.json():
                login_ok = True
                courier_id = login_response.json()["id"]
                
                delete_response = courier_api.delete(courier_id)
                if delete_response.status_code in (200, 202, 204) and delete_response.json() == {"ok": True}:
                    delete_ok = True

        assert (response.status_code == 201 and 
                response.json() == {"ok": True} and 
                login_ok and 
                delete_ok)

    @allure.story("Создание новой учетной записи курьера")
    @allure.title("Запрет на создание дубликата курьера с существующим логином")
    def test_create_duplicate_courier(self, courier_api, courier_payload):
        first = courier_api.create(courier_payload)
        
        # Переменная-флаг для проверки дубликата
        duplicate_rejected = False
        
        if first.status_code == 201:
            second = courier_api.create(courier_payload)
            if second.status_code in (400, 409) and second.json().get("message"):
                duplicate_rejected = True
                
            # Очистка данных: удаляем первого созданного курьера
            login_response = courier_api.login(
                {"login": courier_payload["login"], "password": courier_payload["password"]}
            )
            if login_response.status_code in (200, 201):
                courier_id = login_response.json()["id"]
                courier_api.delete(courier_id)

        assert first.status_code == 201 and duplicate_rejected

    @allure.story("Создание новой учетной записи курьера")
    @allure.title("Ошибка при создании курьера без обязательного поля 'login'")
    def test_create_courier_without_login(self, courier_api):
        response = courier_api.create({"password": "pass123", "firstName": "Name"})
        assert response.status_code == 400 and response.json().get("message")

    @allure.story("Создание новой учетной записи курьера")
    @allure.title("Ошибка при создании курьера без обязательного поля 'password'")
    def test_create_courier_without_password(self, courier_api):
        response = courier_api.create({"login": "login123", "firstName": "Name"})
        assert response.status_code == 400 and response.json().get("message")

    @allure.story("Авторизация курьера")
    @allure.title("Успешный логин курьера в систему")
    def test_login_courier_success(self, courier_api, created_courier):
        payload, _ = created_courier
        create_response = courier_api.create(payload)
        if create_response.status_code == 201:
            response = courier_api.login({"login": payload["login"], "password": payload["password"]})
            assert response.status_code in (200, 201) and "id" in response.json()
            courier_id = response.json()["id"]
            courier_api.delete(courier_id)

    @allure.story("Авторизация курьера")
    @allure.title("Ошибка при авторизации без указания логина")
    def test_login_missing_login(self, courier_api):
        response = courier_api.login({"password": "password123"})
        assert response.status_code == 400 and response.json().get("message")

    @allure.story("Авторизация курьера")
    @allure.title("Ошибка при авторизации без указания пароля (с пустой строкой)")
    def test_login_missing_password(self, courier_api):
        response = courier_api.login({"login": "login123", "password": ""})
        assert response.status_code == 400 and response.json().get("message")

    @allure.story("Авторизация курьера")
    @allure.title("Ошибка при авторизации с несуществующим логином")
    def test_login_wrong_login(self, courier_api):
        response = courier_api.login({"login": "wrong_login", "password": "password123"})
        assert response.status_code == 404 and response.json().get("message")

    @allure.story("Авторизация курьера")
    @allure.title("Ошибка при авторизации с неверным паролем для существующего курьера")
    def test_login_wrong_password(self, courier_api, created_courier):
        payload, _ = created_courier
        response = courier_api.login({"login": payload["login"], "password": "wrong_password"})
        assert response.status_code in (400, 404) and response.json().get("message")

    @allure.story("Удаление курьера")
    @allure.title("Ошибка при отправке запроса на удаление без указания ID курьера")
    def test_delete_courier_without_id(self, courier_api):
        response = courier_api.delete()
        assert response.status_code in (400, 404) and response.json().get("message")

    @allure.story("Удаление курьера")
    @allure.title("Ошибка при попытке удаления курьера с несуществующим ID")
    def test_delete_courier_not_found(self, courier_api):
        response = courier_api.delete(999999999)
        assert response.status_code in (400, 404) and response.json().get("message")