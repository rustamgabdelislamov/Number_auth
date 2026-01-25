from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, UpdateView
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from users.forms import UserRegistrationForm
from users.models import CustomUser, PhoneNumberCodes, InviteRegistration
from users.serializers import (
    PhoneInputSerializer,
    CustomUserSerializer,
    InviteRegistrationSerializer,
    UserInviteSerializer,
    UserDetailSerializer,
)
from users.services import get_relevance_number, generate_invite_code
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny, IsAuthenticated


def logout_view(request):
    logout(request)
    return redirect("/")


class PhoneNumberCode(View):
    """Класс для получения номера телефона и оправки кода на номер через сервер рассылки SMS-AERO"""

    def get(self, request, *args, **kwargs):
        return render(request, "users/phone_number.html")

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        PhoneNumberCodes.objects.all().delete()
        code_auth = generate_invite_code()
        if form.is_valid():
            phone = form.cleaned_data["phone_number"]
            request.session["phone_number"] = phone
            phone_auth = get_relevance_number(phone, code_auth)

            if phone_auth.get("data")["text"] == code_auth:
                PhoneNumberCodes.objects.create(
                    phone=phone, code=code_auth, is_active=True
                )
                print("DEBUG3", PhoneNumberCodes.code)

                return HttpResponseRedirect("code/")
            else:
                messages.error(
                    request, "Что-то пошло не так. Пожалуйста, попробуйте снова."
                )
                return render(request, "users/phone_number.html", {"form": form})
        else:
            # Если форма не валидна, возвращаем ее с ошибками
            return render(request, "users/phone_number.html", {"form": form})


class PhoneNumberCodesCode(View):
    """Класс получения кода от пользователя и сравнения кода из ответа сервиса, если они равны то подтверждаем номер"""

    def get(self, request, *args, **kwargs):
        return render(request, "users/code.html")

    def post(self, request, *args, **kwargs):
        phone = request.session.get("phone_number")
        code = request.POST.get("code")
        phone_number_codes = PhoneNumberCodes.objects.filter(phone=phone).first()
        your_invite = generate_invite_code()
        if phone_number_codes.code == code:

            user = CustomUser.objects.filter(phone_number=phone).first()
            if not user:
                user = CustomUser.objects.create(
                    phone_number=phone, your_invite=your_invite
                )
                user.set_password(code)
                user.save()
            phone_number_codes.delete()
            return HttpResponseRedirect("invite")
        else:
            messages.error(request, "Код не активен или не найден.")
            return render(request, "users/code.html")


class PhoneNumberSomeoneInvite(View):
    """Класс предлагающий ввести реферальный код"""

    def get(self, request, *args, **kwargs):
        return render(request, "users/someone_invite.html")

    def post(self, request, *args, **kwargs):
        phone = request.session.get("phone_number")
        someone_invite = request.POST.get("someone_invite")
        user = CustomUser.objects.get(phone_number=phone)
        if someone_invite:
            invite_owner = CustomUser.objects.filter(your_invite=someone_invite).first()
            if invite_owner:
                InviteRegistration.objects.create(
                    invited_user=invite_owner, user=user, someone_invite=someone_invite
                )
                user.someone_invite = someone_invite
                user.save()
                messages.success(request, "Регистрация завершена успешно!")
            else:
                messages.error(request, "Пользователь не найден.")
                return HttpResponseRedirect(reverse("users:invite"))
        else:
            messages.warning(request, "Реферальная ссылка не создана. Номер подтвержден. ")

        return HttpResponseRedirect(
            reverse("users:home")
        )  # Перенаправление на страницу успеха


class AddInviteView(UpdateView):
    model = CustomUser
    fields = ["someone_invite"]  # Поле, которое будем редактировать
    template_name = "users/someone_invite.html"  # Шаблон страницы изменения
    success_message = "Ваш пригласительный код успешно привязан!"
    success_url = reverse_lazy(
        "users:home"
    )  # Куда переадресовать после успешного обновления

    def get_object(self, queryset=None):
        """
        Получаем объект пользователя, которого хотим обновить.
        """
        return self.request.user

    def form_valid(self, form):
        """
        Действия после успешной отправки формы.
        """
        someone_invite = form.cleaned_data["someone_invite"]

        # Поиск владельца инвайта
        invite_owner = CustomUser.objects.filter(your_invite=someone_invite).first()

        if invite_owner:
            # Сохраняем пользователя только если нашелся владелец инвайта
            form.instance.someone_invite = someone_invite
            form.save()

            # Регистрируем подключение
            InviteRegistration.objects.create(
                invited_user=invite_owner,
                user=self.object,
                someone_invite=someone_invite,
            )
            messages.success(self.request, self.success_message)
        else:
            # Информируем пользователя об ошибке и прерываем операцию
            messages.error(
                self.request, "Пользователь с данным пригласительным кодом не найден."
            )
            return HttpResponseRedirect(
                reverse("users:invite_update")
            )  # Возвращаемся назад без сохранения

        return super().form_valid(form)


class PhoneNumberList(ListView):
    """Класс вывода информации на главную страницу в зависимости от разрешений"""

    model = CustomUser
    template_name = "users/home.html"
    context_object_name = "phone_list"

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            # Перенаправляем не аутентифицированных пользователей на страницу входа
            return HttpResponseRedirect(reverse("users:home"))

        elif user.is_staff:
            # Админ может посмотреть всех аутентифицированных пользователей
            queryset = CustomUser.objects.all()
            return queryset

        else:
            # Обычный пользователь видит только людей подписанных на него через someone_invite
            # .select_related('user') добавлена для оптимизации (чтобы не было лишних запросов к БД)
            return InviteRegistration.objects.filter(invited_user=user).select_related(
                "user"
            )


class PhoneNumberCodeAPIView(APIView):
    """API Класс для получения номера телефона и оправки кода на номер через сервер рассылки SMS-AERO"""

    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Отправьте номер телефона для регистрации."})

    def post(self, request):
        PhoneNumberCodes.objects.all().delete()
        code_auth = generate_invite_code()
        # 1. Передаем данные в сериализатор
        serializer = PhoneInputSerializer(data=request.data)

        # 2. Запускаем валидацию (выполнится validate_phone_number)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 3. Получаем уже очищенный номер (например, 79991234567)
        phone = serializer.validated_data["phone_number"]
        request.session["phone_number"] = phone
        phone_auth = get_relevance_number(phone, code_auth)

        if phone_auth.get("data")["text"] == code_auth:
            PhoneNumberCodes.objects.create(phone=phone, code=code_auth, is_active=True)
            return Response({"message": "Код отправлен."}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Что-то пошло не так. Пожалуйста, попробуйте снова."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PhoneNumberCodesCodeAPIView(APIView):
    """API Класс получения кода от пользователя и сравнения кода из ответа сервиса,
    если они равны то подтверждаем номер"""

    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Введите код для подтверждения."})

    def post(self, request):
        phone = request.session.get("phone_number")
        code = request.data.get("code")

        if not phone or not code:
            return Response(
                {"error": "Номер телефона или код не предоставлены."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        phone_number_codes = PhoneNumberCodes.objects.filter(phone=phone).first()

        your_invite = generate_invite_code()

        if phone_number_codes and phone_number_codes.code == code:
            user = CustomUser.objects.filter(phone_number=phone).first()
            if not user:
                user = CustomUser.objects.create(
                    phone_number=phone, your_invite=your_invite
                )
                user.set_password(code)
                user.save()
            phone_number_codes.delete()
            return Response(
                {"message": "Регистрация завершена успешно!"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": "Код не активен или не найден."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PhoneNumberSomeoneInviteAPI(APIView):
    """Класс предлагающий ввести реферальный код"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Введите реферальный код."})

    def post(self, request, *args, **kwargs):
        phone = request.session.get("phone_number")
        someone_invite = request.data.get("someone_invite")

        user = CustomUser.objects.get(phone_number=phone)
        user.someone_invite = someone_invite
        user.save()

        if someone_invite:
            invite_owner = CustomUser.objects.filter(your_invite=someone_invite).first()

            if invite_owner:
                InviteRegistration.objects.create(
                    invited_user=invite_owner, user=user, someone_invite=someone_invite
                )
                return Response(
                    {"message": "Регистрация завершена успешно!"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": "Пользователь не найден."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"warning": "Реферальная ссылка не создана"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AddInviteAPIView(generics.UpdateAPIView):
    serializer_class = UserInviteSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Возвращаем текущего пользователя
        return self.request.user

    def perform_update(self, serializer):
        # Выполняем стандартное обновление, плюс дополнительную логику для связи владельцев
        instance = serializer.save()
        someone_invite = serializer.validated_data["someone_invite"]
        invite_owner = CustomUser.objects.get(your_invite=someone_invite)
        InviteRegistration.objects.create(
            invited_user=invite_owner, user=instance, someone_invite=someone_invite
        )


class PhoneNumberListAPI(generics.ListAPIView):
    """API для вывода информации о пользователях в зависимости от разрешений"""

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user

        if user.is_staff:
            return CustomUserSerializer
        else:
            return InviteRegistrationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            # Админ может увидеть всех аутентифицированных пользователей
            return CustomUser.objects.all()
        else:
            # Обычный пользователь видит только тех, кто подписан на него
            return InviteRegistration.objects.filter(invited_user=user).select_related(
                "user"
            )


class MyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Авторизованный пользователь

        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
