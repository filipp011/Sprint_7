import pytest
import requests
from data import API_CREATE_ORDER_URL
import allure

@allure.feature("Create Order")
class TestCreateOrder:

    # Заказ только черного самоката
    @allure.story("Order with different colors")
    @pytest.mark.parametrize("color, expected_status", [
        (["BLACK"], 201),  # Один цвет - BLACK
        (["GREY"], 201),   # Один цвет - GREY
        (["BLACK", "GREY"], 201),  # Оба цвета
        ([], 201)  # Без указания цвета
    ])
    def test_create_order(self, color, expected_status):
        payload = {
            "firstName": "Иван",
            "lastName": "Петрович",
            "address": "Уляп, 142 дом.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": color
        }
        
        response = requests.post(API_CREATE_ORDER_URL, json=payload)

        # Проверяем, что статус-код ответа соответствует ожидаемому
        assert response.status_code == expected_status

    # При успешном заказе выдает track
    @allure.story("Successful order returns track")
    def test_create_order_have_track(self):
        payload = {
            "firstName": "Иван",
            "lastName": "Петрович",
            "address": "Уляп, 142 дом.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": ["BLACK", "GREY"]
        }
        
        response = requests.post(API_CREATE_ORDER_URL, json=payload)

        # Проверяем, что в ответе содержится track
        response_data = response.json()
        assert "track" in response_data

