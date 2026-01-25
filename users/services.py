import os
import random
import string

import requests
from dotenv import load_dotenv


load_dotenv()


def generate_invite_code(length=6):
    """Генератор инвайт кода и кода для авторизации"""
    characters = string.ascii_letters + string.digits  # Символы: буквы и цифры
    invite_code = "".join(random.choice(characters) for _ in range(length))
    return invite_code


def get_relevance_number(phone_number, text):
    """Функция для получения кода через SMS Aero"""
    url = os.getenv("URL")
    your_api_key = os.getenv("YOUR_API_KEY")
    email = os.getenv("EMAIL")
    "https://email:api_key@gate.smsaero.ru/v2/sms/send?number=79990000000&text=your+text&sign=SMS Aero"

    response = requests.get(
        f"https://{email}:{your_api_key}@{url}={phone_number}&text={text}&sign=SMS Aero"
    )
    if response.status_code == 200:
        print("Сообщение успешно отправлено!")
        return response.json()
    else:
        print(f"Ошибка: {response.status_code} - {response.text}")
    # заглушка имитации отправки кода
    # from users.views import code_auth
    # data = {
    #     "success": "true",
    #     "data": [
    #         {
    #             "id": 1,
    #             "from": "SMS Aero",
    #             "number": "79990000000",
    #             "text": code_auth,
    #             "status": 0,
    #             "extendStatus": "queue",
    #             "channel": "FREE SIGN",
    #             "cost": 1.95,
    #             "dateCreate": 1510656981,
    #             "dateSend": 1510656981
    #         }]
    # }
    # print(data)
    # return data
