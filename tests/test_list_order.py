import requests
from data import API_LIST_ORDER_URL
import allure

@allure.feature("Список заказов")
class TestListOrder:

    @allure.story("Получение списка заказов")
    def test_orders_list(self):
        response = requests.get(API_LIST_ORDER_URL)
        response_data = response.json()
        # Проверяем, что значение по ключу "orders" является списком и не пустое
        orders = response_data.get("orders")
        assert isinstance(orders, list) and len(orders) > 0
