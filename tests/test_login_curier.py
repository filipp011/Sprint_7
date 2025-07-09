import pytest
import requests
from data import API_LOGIN_URL
import allure

@allure.feature("Вход курьера")
class TestLoginCurier:

    @pytest.mark.parametrize("login, password, expected_status, expected_message", [
    ("", "558855", 400, "Недостаточно данных для входа"),  # Пустой логин
    (None, "558855", 400, "Недостаточно данных для входа")  # Отсутствие поля логина
])
    @allure.story("Проверка ошибок при входе курьера")
    def test_courier_login_errors(self, login, password, expected_status, expected_message):
        url = API_LOGIN_URL
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(url, json=payload)
        response_data = response.json()
        
        # Проверяем, что статус-код ответа соответствует ожидаемому
        assert response.status_code == expected_status
        assert response_data.get("message") == expected_message
        

    @allure.story("Курьер не найден")
    def test_courier_not_found(self):
        url = API_LOGIN_URL
        payload = {
            "login": "петручо",
            "password": "558855"
        }
        response = requests.post(url, json=payload)
        response_data = response.json()
        # Проверяем, что статус-код ответа 404 (не найдено)
        assert response.status_code == 404 and response_data.get("message") == "Учетная запись не найдена"


    @allure.story("Успешный вход возвращает id")
    def test_courier_get_id(self):
        url = API_LOGIN_URL
        payload = {
            "login": "Filipp",
            "password": "558855"
        }
        response = requests.post(url, json=payload)
        # Проверяем, что в ответе содержится id
        response_data = response.json()
        assert "id" in response_data and response.status_code == 200
