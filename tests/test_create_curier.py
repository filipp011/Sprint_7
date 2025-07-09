import requests
import pytest
import allure
from data import API_CREATE_URL

@allure.suite("Тесты регистрации курьера")
class TestCreateCourier:

    @allure.title("Тест регистрации нового курьера")
    @allure.description("Проверка успешной регистрации нового курьера.")
    def test_registration_courier(self, courier):

        # Используем данные из фикстуры
        login = courier[1]
        password = courier[1]
        
        # Собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": login
        }
        
        # Отправка POST-запроса
        response = requests.post(API_CREATE_URL, json=payload)
        assert response.status_code == 201 and response.json() == {"ok": True}


    @allure.title("Тест дублирования регистрации курьера")
    @allure.description("Проверка, что регистрация курьера с теми же логином, паролем и именем завершается неудачей.")
    def test_duplicate_courier_registration(self):

        # Собираем тело запроса для первого курьера
        payload = {
            "login": "ninja",
            "password": "1234",
            "firstName": "saske"
        }
        # Отправка POST-запроса для создания второго курьера с теми же данными
        duplicate_response = requests.post(API_CREATE_URL, json=payload)
        response_json = duplicate_response.json()
        # Проверка статуса ответа на попытку создания дубликата и сообщение
        assert duplicate_response.status_code == 409 and response_json.get("message") == "Этот логин уже используется. Попробуйте другой." 


    @pytest.mark.parametrize("login, password, expected_status", [
        ("", "valid_password", 400),  # Пустой логин
        ("valid_login", "", 400)       # Пустой пароль
    ])
    @allure.title("Тест создания курьера с пустым логином или паролем")
    @allure.description("Проверка, что возвращается код состояния 400, когда логин или пароль пустые.")
    def test_courier_creation_empty_login_or_password(self, login, password, expected_status):
        
        # Собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": "Test"
        }

        response = requests.post(API_CREATE_URL, json=payload)
        response_data = response.json()

        # Проверяем, что статус-код ответа соответствует ожидаемому и сообщение
        assert response.status_code == expected_status and response_data["message"] == "Недостаточно данных для создания учетной записи"
        

    @allure.title("Тест дублирования регистрации курьера по логину")
    @allure.description("Проверка, что регистрация курьера с тем же логином завершается неудачей.")
    def test_duplicate_courier_login_registration(self):

        # Собираем тело запроса для первого курьера
        payload = {
            "login": "ninja",
            "password": "1565",
            "firstName": "аghfd"
        }
        # Отправка POST-запроса для создания второго курьера с теми же данными
        duplicate_login = requests.post(API_CREATE_URL, json=payload)
        response_data = duplicate_login.json()
        # Проверка статуса ответа на попытку создания дубликата по логину и сообщение
        assert duplicate_login.status_code == 409 and response_data["message"] == "Этот логин уже используется. Попробуйте другой."
