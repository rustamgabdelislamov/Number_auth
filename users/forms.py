from users.models import CustomUser
from django import forms

from users.validators import normalize_and_validate_phone


class UserRegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=17,
        help_text="Обязательное поле. Введите номер телефона",
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        return normalize_and_validate_phone(phone_number, check_exists=True)

    class Meta:
        model = CustomUser
        fields = ["phone_number"]
