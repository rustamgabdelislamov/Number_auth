from django.db.models import Subquery, OuterRef
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
        fields = ["id", "phone_number", "your_invite", "someone_invite"]


class InviteRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteRegistration
        fields = [
            "id",
            "invited_user",
            "user",
            "someone_invite",
            "created_at",
        ]  # или перечислите необходимые поля


class UserInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("someone_invite",)

    def validate_someone_invite(self, value):
        # Проверяем, существует ли владелец данного приглашения
        if not CustomUser.objects.filter(your_invite=value).exists():
            raise serializers.ValidationError(
                "Пользователь с данным пригласительным кодом не найден."
            )
        return value


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteRegistration
        fields = ("id", "user_id", "user_phone", "created_at")

    user_phone = serializers.ReadOnlyField(source="user.phone_number")


class UserDetailSerializer(serializers.ModelSerializer):
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'phone_number', 'your_invite', 'referrals')

    def get_referrals(self, obj):
        # Строим подзапрос, который выбирает максимальную дату регистрации для каждого пользователя
        subquery = InviteRegistration.objects.filter(user=OuterRef('user'), invited_user=obj).order_by('-created_at')

        # Получаем уникальный список пользователей с самыми последними регистрациями
        result = InviteRegistration.objects.filter(
            user__in=subquery.values('user'),
            created_at=Subquery(subquery.values('created_at')[:1])
        ).distinct()

        return ReferralSerializer(result, many=True).data
