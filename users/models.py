from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(
        unique=True,
        max_length=15,
        verbose_name="Телефон",
        help_text="Обязательное поле. Введите номер телефона",
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
        return str(self.phone_number)

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class PhoneNumberCodes(models.Model):
    phone = models.CharField(
        max_length=15,
        verbose_name="Телефон",
        help_text="Обязательное поле. Введите номер телефона",
    )
    code = models.CharField(
        verbose_name="Код для подтверждения",
    )
    is_active = models.BooleanField(default=True)


class InviteRegistration(models.Model):
    invited_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='invite',
        verbose_name="Хозяин инвайта"
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name="тот кто зарегистрировался"
    )
    someone_invite = models.CharField(
        max_length=6,
        verbose_name="Инвайт код"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")


    class Meta:
        verbose_name = "Регистрация по инвайт коду"
        verbose_name_plural = "Регистрации по инвайт кодам"

    def __str__(self):
        return f"{self.user} зарегистрирован по коду {self.someone_invite} пользователя {self.invited_user.phone_number}"
