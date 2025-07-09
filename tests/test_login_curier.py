import requests
from data import API_LOGIN_URL
import allure

@allure.feature("Вход курьера")
class TestLoginCurier:

    @allure.story("Ошибка при пустом логине")
    def test_courier_not_login(self):
        url = API_LOGIN_URL
        payload = {
            "login": "",
            "password": "558855"
        }
        response = requests.post(url, json=payload)
        response_data = response.json()
        # Проверяем, что статус-код ответа 400 (ошибка)
        assert response.status_code == 400 and response_data.get("message") == "Недостаточно данных для входа"


    @allure.story("Ошибка при отсутствии поля логина")
    def test_courier_no_field(self):
        url = API_LOGIN_URL
        payload = {
            "password": "558855"
        }
        response = requests.post(url, json=payload)
        response_data = response.json()
        # Проверяем, что статус-код ответа 400 (ошибка)
        assert response.status_code == 400 and response_data.get("message") == "Недостаточно данных для входа"
        

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
