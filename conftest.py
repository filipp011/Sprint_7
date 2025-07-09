import pytest
import requests
from helpers import register_new_courier_and_return_login_password

# Фикстура для регистрации курьера
@pytest.fixture
def courier():
    # Регистрация нового курьера и получение логина и пароля
    login_pass = register_new_courier_and_return_login_password()
    
    # Возвращаем логин и пароль
    yield login_pass
    
    # Удаление курьера после теста
    if login_pass:
        login = login_pass[0]
        # Отправка запроса на удаление курьера
        delete_url = f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{login}'
        requests.delete(delete_url)

