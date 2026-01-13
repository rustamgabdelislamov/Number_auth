from rest_framework import serializers

from users.models import CustomUser, InviteRegistration
from users.validators import normalize_and_validate_phone

class PhoneInputSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        # Вызываем нашу внешнюю функцию
        return normalize_and_validate_phone(value)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class InviteRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteRegistration
        fields = '__all__'  # или перечислите необходимые поля
