import requests
from data import API_LOGIN_URL
import allure

@allure.feature("Courier Login")
class TestLoginCurier:

    @allure.story("Courier can log in")
    def test_courier_login(self):
        url = API_LOGIN_URL
        payload = {
            "login": "Filipp",
            "password": "558855"
        }
        response = requests.post(url, json=payload)
    
        # Проверяем, что статус-код ответа 200 (успешный запрос)
        assert response.status_code == 200

    @allure.story("Error when login is empty")
    def test_courier_not_login(self):
        url = API_LOGIN_URL
        payload = {
            "login": "",
            "password": "558855"
        }
        response = requests.post(url, json=payload)
    
        # Проверяем, что статус-код ответа 400 (ошибка)
        assert response.status_code == 400

    @allure.story("Error when login field is missing")
    def test_courier_no_field(self):
        url = API_LOGIN_URL
        payload = {
            "password": "558855"
        }
        response = requests.post(url, json=payload)
    
        # Проверяем, что статус-код ответа 400 (ошибка)
        assert response.status_code == 400

    @allure.story("Courier not found")
    def test_courier_not_found(self):
        url = API_LOGIN_URL
        payload = {
            "login": "петручо",
            "password": "558855"
        }
        response = requests.post(url, json=payload)
    
        # Проверяем, что статус-код ответа 404 (не найдено)
        assert response.status_code == 404

    @allure.story("Successful login returns id")
    def test_courier_get_id(self):
        url = API_LOGIN_URL
        payload = {
            "login": "Filipp",
            "password": "558855"
        }
        response = requests.post(url, json=payload)
        # Проверяем, что в ответе содержится id
        response_data = response.json()
        assert "id" in response_data
