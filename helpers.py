import random
import string
import requests

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def register_new_courier_and_return_login_password():
    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    while True:
        # генерируем логин, пароль и имя курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        # собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', json=payload)

        # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
        if response.status_code == 201:
            login_pass.append(login)
            login_pass.append(password)
            login_pass.append(first_name)
            break  # Выходим из цикла, если регистрация успешна
        elif response.status_code == 409:
            # Если курьер с таким логином уже существует, пробуем снова
            continue
        else:
            raise Exception("Failed to register courier")

    # возвращаем список
    return login_pass

