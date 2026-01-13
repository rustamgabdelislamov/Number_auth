from django.core.management import call_command
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import CustomUser, InviteRegistration
from django.core.exceptions import ValidationError
from unittest.mock import patch, Mock
from users.services import generate_invite_code, get_relevance_number
from users.validators import normalize_and_validate_phone


class UserViewSetTests(APITestCase):

    def setUp(self):
        # Создание тестовых пользователей
        self.staff_user = CustomUser.objects.create(
            phone_number="79871371048", your_invite="123456", is_staff=True
        )
        self.staff_user.set_password("password123")
        self.staff_user.save()

        self.normal_user = CustomUser.objects.create(
            phone_number="79000000000",
            password="password123",
            your_invite="111111",
            is_staff=False,
        )
        self.normal_user.set_password("password123")
        self.normal_user.save()

        self.invited_user = CustomUser.objects.create(
            phone_number="79000009999",
            password="password123",
            your_invite="222222",
        )
        self.invited_user.set_password("password123")
        self.invited_user.save()

        # Создание записи для обычного пользователя
        InviteRegistration.objects.create(
            user=self.invited_user,
            invited_user=self.normal_user,
            someone_invite=self.normal_user.your_invite,
        )

    def test_staff_can_see_all_users(self):
        token_url = reverse("users:api_login")  # или ваш путь
        resp = self.client.post(
            token_url,
            {"phone_number": "79871371048", "password": "password123"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK, resp.data
        access = resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        response = self.client.get(reverse("users:api_home"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), CustomUser.objects.count())

    def test_normal_user_can_see_only_invited_users(self):
        token_url = reverse("users:api_login")
        resp = self.client.post(
            token_url,
            {"phone_number": "79000000000", "password": "password123"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK, resp.data
        access = resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        response = self.client.get(reverse("users:api_home"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # Проверка, что обычный пользователь видит только одного приглашенного пользователя
        self.assertEqual(
            response.data[0]["someone_invite"], "111111"
        )  # Проверка, что это именно тот инвайт

    def test_anonymous_user_cannot_access_users(self):
        response = self.client.get(reverse("users:api_home"))

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )  # Проверка, что не авторизованный пользователь не может получить доступ

    def test_valid_phone_number(self):
        self.assertEqual(normalize_and_validate_phone("89001234567"), "79001234567")
        self.assertEqual(normalize_and_validate_phone("70001234567"), "70001234567")

    def test_invalid_starting_digit(self):
        with self.assertRaises(ValidationError) as context:
            normalize_and_validate_phone("60001234567")
        self.assertEqual(
            str(context.exception.args[0]), "Номер должен начинаться с 7 или 8."
        )

    def test_invalid_length(self):
        with self.assertRaises(ValidationError) as context:
            normalize_and_validate_phone("8900123456")  # 10 цифр
        self.assertEqual(
            str(context.exception.args[0]), "Номер должен содержать 11 цифр."
        )

        with self.assertRaises(ValidationError) as context:
            normalize_and_validate_phone("890012345678")  # 12 цифр
        self.assertEqual(
            str(context.exception.args[0]), "Номер должен содержать 11 цифр."
        )

    def test_existing_phone_number(self):
        with self.assertRaises(ValidationError) as context:
            normalize_and_validate_phone("79871371048", check_exists=True)
        self.assertEqual(
            str(context.exception.args[0]), "Этот номер уже зарегистрирован."
        )

    def test_non_existing_phone_number(self):
        self.assertEqual(
            normalize_and_validate_phone("89001234567", check_exists=True),
            "79001234567",
        )

    def test_invite_code_length(self):
        """Проверка длины инвайт-кода"""
        code = generate_invite_code(6)
        self.assertEqual(len(code), 6)

    @patch("requests.get")
    @patch("builtins.print")  # Перехват вывода print
    def test_successful_response(self, mock_print, mock_get):
        """Проверка успешного ответа от API"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_get.return_value = mock_response

        result = get_relevance_number("79990000000", "your text")

        self.assertEqual(result, {"success": True})
        mock_get.assert_called_once()
        mock_print.assert_called_with(
            "Сообщение успешно отправлено!"
        )  # Проверка вывода

    @patch("requests.get")
    @patch("builtins.print")  # Перехват вывода print
    def test_error_response(self, mock_print, mock_get):
        """Проверка обработки ошибки от API"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_get.return_value = mock_response

        result = get_relevance_number("79990000000", "your text")

        self.assertIsNone(result)
        mock_print.assert_called_with("Ошибка: 400 - Bad Request")  # Проверка вывода


class CommandTest(TestCase):
    def setUp(self):
        # Настройка среды для тестирования
        self.users_data = [
            {
                "phone_number": "79876667777",
                "password": "password123",
                "your_invite": "123456",
            },
            {
                "phone_number": "79000000000",
                "password": "password123",
                "your_invite": "111111",
                "someone_invite": "123456",
            },
            {
                "phone_number": "79000005555",
                "password": "password123",
                "your_invite": "222222",
                "someone_invite": "123456",
            },
        ]

    def test_create_users_and_invites(self):
        # Вызов команды управления
        call_command("add_users")  # Замените 'your_command_name' на имя вашей команды

        # Проверка, что пользователи созданы
        users = CustomUser.objects.all()
        self.assertEqual(users.count(), 3)

        # Проверка, что пользователи созданы с правильными данными
        for user_data in self.users_data:
            user = CustomUser.objects.get(phone_number=user_data["phone_number"])
            self.assertEqual(user.your_invite, user_data["your_invite"])

        # Проверка, что реферальные ссылки зарегистрированы
        invites = InviteRegistration.objects.all()
        self.assertEqual(invites.count(), 2)

        # Проверка данных реферальных ссылок
        self.assertTrue(invites.filter(user=users[1], invited_user=users[0]).exists())
        self.assertTrue(invites.filter(user=users[2], invited_user=users[0]).exists())
