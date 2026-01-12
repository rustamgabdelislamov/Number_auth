import re
from users.models import CustomUser
from django import forms


class UserRegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=17,
        help_text="Обязательное поле. Введите номер телефона",)

    def clean_phone_number(self):
        # Получаем данные, введенные пользователем
        phone_number = self.cleaned_data.get('phone_number')

        user_exists = CustomUser.objects.filter(phone_number=phone_number).exists()
        if user_exists:
            raise forms.ValidationError("Такой номер уже существует. Пожалуйста, попробуйте снова.")

        # 1. Удаляем все лишние символы: пробелы, скобки, тире, плюсы
        phone_number = re.sub(r'\D', '', phone_number)

        if not phone_number.startswith('7'):
            raise forms.ValidationError("Номер телефона должен начинаться с 7.")

        # 2. Обработка первой цифры
        # Если номер начинается с 8, меняем на 7
        if phone_number.startswith('8'):
            phone_number = '7' + phone_number[1:]

        # 3. Проверка длины (для РФ номеров это обычно 11 цифр)
        if len(phone_number) != 11:
            raise forms.ValidationError("Номер телефона должен состоять из 11 цифр.")
        print(phone_number)


        return phone_number

    class Meta:
        model = CustomUser
        fields = ['phone_number']
