from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.forms import UserRegistrationForm
from users.models import CustomUser, PhoneNumberCodes, InviteRegistration
from users.services import get_relevance_number, generate_invite_code
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect




def logout_view(request):
    logout(request)
    return redirect("/")

code_auth = generate_invite_code()
print("DEBUG1",code_auth)

class PhoneNumberCode(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/phone_number.html')

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            request.session['phone_number'] = phone
            phone_auth = get_relevance_number(phone, code_auth)
            if phone_auth.get("data")[0]["text"] == code_auth:
                PhoneNumberCodes.objects.create(phone=phone, code=code_auth, is_active=True)

                return HttpResponseRedirect("code/")
            else:
                messages.error(request, "Что-то пошло не так. Пожалуйста, попробуйте снова.")
                return render(request, 'users/phone_number.html', {'form': form})
        else:
            # Если форма не валидна, возвращаем ее с ошибками
            return render(request, 'users/phone_number.html', {'form': form})


class PhoneNumberCodesCode(View):
    MAX_ATTEMPTS = 3
    def get(self, request, *args, **kwargs):
        return render(request, 'users/code.html')

    def post(self, request, *args, **kwargs):
        phone = request.session.get('phone_number')
        code = request.POST.get("code")
        print("DEBUG2", code)
        # attempts = request.session.get('attempts', 0)
        phone_number_codes = PhoneNumberCodes.objects.filter(phone=phone).first()
        your_invite = generate_invite_code()
        print("DEBUG3", phone_number_codes.code)
        # if attempts < self.MAX_ATTEMPTS:
        if phone_number_codes.code == code:

            user = CustomUser.objects.filter(phone_number=phone).first()
            if not user:
                user = CustomUser.objects.create(phone_number=phone, your_invite=your_invite)
                user.set_password(code)
                user.save()
            phone_number_codes.delete()
            return HttpResponseRedirect("invite")
        else:
            # attempts += 1  # Увеличиваем количество попыток
            # request.session['attempts'] = attempts
            messages.error(request, "Код не активен или не найден.")
            return render(request, 'users/code.html')
        # else:
        #     messages.error(request, "Превышено максимальное количество попыток.")
        #
        #     return HttpResponseRedirect(reverse('users:home'))


class PhoneNumberSomeoneInvite(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/someone_invite.html')

    def post(self, request, *args, **kwargs):
        phone = request.session.get('phone_number')
        someone_invite = request.POST.get("someone_invite")
        print("DEBUG5", someone_invite)
        print("DEBUG6", phone)

        user = CustomUser.objects.get(phone_number=phone)
        user.someone_invite = someone_invite
        user.save()

        if someone_invite:
            invite_owner = CustomUser.objects.filter(your_invite=someone_invite).first()
            print("DEBUG7", invite_owner)

            if invite_owner:

                InviteRegistration.objects.create(invited_user=invite_owner, user=user, someone_invite=someone_invite)
                messages.success(request, "Регистрация завершена успешно!")
            else:
                print(1)
                messages.error(request, "Пользователь не найден.")
                return HttpResponseRedirect(reverse("users:invite"))
        else:
            messages.warning(request, "Реферальная ссылка не создана")

        return HttpResponseRedirect(reverse('users:home'))  # Перенаправление на страницу успеха


class PhoneNumberList(ListView):
    model = CustomUser
    template_name = 'users/home.html'
    context_object_name = 'phone_list'



    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            # Перенаправляем неаутентифицированных пользователей на страницу входа
            return HttpResponseRedirect(reverse('users:home'))

        elif user.is_staff:
            queryset = CustomUser.objects.all()
            return queryset


        else:
            # Обычный пользователь видит только людей подписанных на него через someone_invite
            # .select_related('user') добавлена для оптимизации (чтобы не было лишних запросов к БД)
            return InviteRegistration.objects.filter(invited_user=user).select_related('user')


class PhoneNumberCodeAPIView(APIView):
    def get(self, request):
        return Response({"message": "Отправьте номер телефона для регистрации."})

    def post(self, request):
        phone = request.data.get('phone_number')

        if not phone:
            return Response({"error": "Номер телефона не предоставлен."}, status=status.HTTP_400_BAD_REQUEST)

        request.session['phone_number'] = phone
        phone_auth = get_relevance_number(phone, code_auth)

        if phone_auth.get("data")[0]["text"] == code_auth:
            PhoneNumberCodes.objects.create(phone=phone, code=code_auth, is_active=True)
            return Response({"message": "Код отправлен."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Что-то пошло не так. Пожалуйста, попробуйте снова."},
                            status=status.HTTP_400_BAD_REQUEST)


class PhoneNumberCodesCodeAPIView(APIView):

    def get(self, request):
        return Response({"message": "Введите код для подтверждения."})

    def post(self, request):
        phone = request.session.get('phone_number')
        code = request.data.get("code")

        if not phone or not code:
            return Response({"error": "Номер телефона или код не предоставлены."}, status=status.HTTP_400_BAD_REQUEST)

        phone_number_codes = PhoneNumberCodes.objects.filter(phone=phone).first()
        your_invite = generate_invite_code()

        if phone_number_codes and phone_number_codes.code == code:
            user = CustomUser.objects.filter(phone_number=phone).first()
            if not user:
                user = CustomUser.objects.create(phone_number=phone, your_invite=your_invite)
                user.set_password(code)
                user.save()
            phone_number_codes.delete()
            return Response({"message": "Регистрация завершена успешно!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Код не активен или не найден."}, status=status.HTTP_400_BAD_REQUEST)


