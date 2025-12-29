from django.db.models import BooleanField
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():  # Ключ (field_name) — это строка, обозначающая имя поля («title», «content», «price» и т.п.).Значение (field) — это экземпляр конкретного класса поля, например, CharField, IntegerField, BooleanField и т.д., наследующие от базового класса полей Django.
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = "__all__"
