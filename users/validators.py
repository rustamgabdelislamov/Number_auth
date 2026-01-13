import re
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


def normalize_and_validate_phone(value, check_exists=False):
    """
    Универсальная функция:
    1. Очищает номер.
    2. Валидирует формат.
    3. (Опционально) Проверяет наличие в базе.
    """
    # Очистка от мусора
    phone = re.sub(r'\D', '', value)

    if phone.startswith('8'):
        phone = '7' + phone[1:]

    # Базовая валидация
    if not phone.startswith('7'):
        raise ValidationError("Номер должен начинаться с 7 или 8.")

    if len(phone) != 11:
        raise ValidationError("Номер должен содержать 11 цифр.")

    # Проверка на существование (если нужно)
    User = get_user_model()
    if check_exists and User.objects.filter(phone_number=phone).exists():
        raise ValidationError("Этот номер уже зарегистрирован.")

    return phone
