import requests
import pytest
import allure
from data import API_CREATE_URL
from utils import register_new_courier_and_return_login_password

@allure.suite("Тесты регистрации курьера")
class TestCreateCourier:

    @allure.title("Тест регистрации нового курьера")
    @allure.description("Проверка успешной регистрации нового курьера.")
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

    @allure.title("Тест дублирования регистрации курьера")
    @allure.description("Проверка, что регистрация курьера с теми же логином, паролем и именем завершается неудачей.")
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
        response_json = duplicate_response.json()
        # Проверка статуса ответа на попытку создания дубликата
        assert duplicate_response.status_code == 409 and response_json.get("message") == "Этот логин уже используется. Попробуйте другой."  # Ожидаем статус 409 Conflict и сообщение

    @allure.title("Тест успешного создания курьера")
    @allure.description("Проверка, что ответ содержит {'ok': true} после успешной регистрации.")
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
        assert response.json() == {"ok": True} and response.status_code == 201

    @pytest.mark.parametrize("login, password, expected_status", [
        ("", "valid_password", 400),  # Пустой логин
        ("valid_login", "", 400)       # Пустой пароль
    ])
    @allure.title("Тест создания курьера с пустым логином или паролем")
    @allure.description("Проверка, что возвращается код состояния 400, когда логин или пароль пустые.")
    def test_courier_creation_empty_login_or_password(self, login, password, expected_status):
        url = API_CREATE_URL
        
        # Собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": "Test"
        }

        response = requests.post(url, json=payload)
        response_data = response.json()

        # Проверяем, что статус-код ответа соответствует ожидаемому и сообщение
        assert response.status_code == expected_status and response_data["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Тест дублирования регистрации курьера по логину")
    @allure.description("Проверка, что регистрация курьера с тем же логином завершается неудачей.")
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
        response_data = duplicate_login.json()
        # Проверка статуса ответа на попытку создания дубликата по логину и сообщение
        assert duplicate_login.status_code == 409 and response_data["message"] == "Этот логин уже используется. Попробуйте другой."
