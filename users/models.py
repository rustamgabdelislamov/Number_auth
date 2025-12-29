from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Телефон",
        help_text="Обязательное поле. Введите номер телефона",
    )
    is_true = models.BooleanField(
        default=False,
        verbose_name="Актуальность номера",
    )
    your_invite = models.CharField(
        max_length=6,
        verbose_name="Свой инвайт код"
    )
    someone_invite = models.CharField(
        max_length=6,
        verbose_name="Чужой инвайт код",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
