from django.core.management import BaseCommand

from users.models import CustomUser, InviteRegistration


class Command(BaseCommand):
    help = "Создаем 3 пользователей и реферальные ссылки"

    def handle(self, *args, **options):
        users = []

        users_data = [
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

        for user_data in users_data:
            # Удаляем пароль из данных пользователя, если он есть
            password = user_data.pop("password", None)

            # Получаем или создаем пользователя
            user, created = CustomUser.objects.get_or_create(**user_data)

            # Если пользователь был создан, устанавливаем хэшированный пароль
            if created:
                if password:
                    user.set_password(password)  # Хэшируем пароль
                    user.save()  # Сохраняем изменения в базе данных
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added user: {user.phone_number}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"User already exists: {user.phone_number}")
                )

            users.append(user)

        invite_data = [
            {"invited_user": users[0], "user": users[1], "someone_invite": "123456"},
            {"invited_user": users[0], "user": users[2], "someone_invite": "123456"},
        ]

        for invite in invite_data:
            payment, created = InviteRegistration.objects.get_or_create(**invite)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Зарегистрировали: {invite["user"]}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Не зарегестрировали: {invite["user"]}")
                )
