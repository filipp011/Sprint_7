import requests
import pytest
import allure
from data import API_CREATE_URL
from utils import register_new_courier_and_return_login_password

@allure.suite("Courier Registration Tests")
class TestCreateCourier:

    @allure.title("Test Registration of a New Courier")
    @allure.description("Verify that a new courier can be registered successfully.")
    def test_registration_courier(self):
        url = API_CREATE_URL
        login_pass = register_new_courier_and_return_login_password()
        # Собираем тело запроса
        payload = {
            "login": login_pass[1],
            "password": login_pass[1],
            "firstName": login_pass[1]
        }
        
        # Отправка POST-запроса
        response = requests.post(url, json=payload)
        
        # Проверка статуса ответа
        assert response.status_code == 201 and response.json() == {"ok": True}

    @allure.title("Test Duplicate Courier Registration")
    @allure.description("Verify that registering a courier with the same login, password, and name fails.")
    def test_duplicate_courier_registration(self):
        url = API_CREATE_URL

        # Собираем тело запроса для первого курьера
        payload = {
            "login": "ninja",
            "password": "1234",
            "firstName": "saske"
        }
        # Отправка POST-запроса для создания второго курьера с теми же данными
        duplicate_response = requests.post(url, json=payload)

        # Проверка статуса ответа на попытку создания дубликата
        assert duplicate_response.status_code == 409 and response_json.get("message") == "Этот логин уже используется. Попробуйте другой." # Ожидаем статус 409 Conflict и сообщение

    @allure.title("Test Successful Courier Creation")
    @allure.description("Verify that the response contains {'ok': true} after successful registration.")
    def test_successful_courier_creation(self):
        url = API_CREATE_URL
        login_pass = register_new_courier_and_return_login_password()
        # Собираем тело запроса
        payload = {
            "login": login_pass[1],
            "password": login_pass[1],
            "firstName": login_pass[1]
        }
        response = requests.post(url, json=payload)

        # Проверяем, что ответ содержит {"ok": true}
        assert response.json() == {"ok": True}

    @pytest.mark.parametrize("login, password, expected_status", [
        ("", "valid_password", 400),  # Пустой логин
        ("valid_login", "", 400)       # Пустой пароль
    ])
    @allure.title("Test Courier Creation with Empty Login or Password")
    @allure.description("Verify that a 400 status code is returned when login or password is empty.")
    def test_courier_creation_empty_login_or_password(self, login, password, expected_status):
        url = API_CREATE_URL
        
        # Собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": "Test"
        }

        response = requests.post(url, json=payload)

        # Проверяем, что статус-код ответа соответствует ожидаемому
        assert response.status_code == expected_status

    @allure.title("Test Duplicate Courier Login Registration")
    @allure.description("Verify that registering a courier with the same login fails.")
    def test_duplicate_courier_login_registration(self):
        url = API_CREATE_URL

        # Собираем тело запроса для первого курьера
        payload = {
            "login": "ninja",
            "password": "1565",
            "firstName": "аghfd"
        }
        # Отправка POST-запроса для создания второго курьера с теми же данными
        duplicate_login = requests.post(url, json=payload)

        # Проверка статуса ответа на попытку создания дубликата
        assert duplicate_login.status_code == 409  # Ожидаем статус 409 Conflict
