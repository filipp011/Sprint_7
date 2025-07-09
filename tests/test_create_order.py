import pytest
import requests
from data import API_CREATE_ORDER_URL
import allure

@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.story("Заказ с разными цветами")
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
            "comment": "Саске, вернись в Коноху",
            "color": color
        }
        
        response = requests.post(API_CREATE_ORDER_URL, json=payload)
        response_data = response.json()

        # Проверяем, что статус-код ответа соответствует ожидаемому
        assert response.status_code == expected_status and "track" in response_data
