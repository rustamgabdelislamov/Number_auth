from django.urls import path
from django.contrib.auth.views import LoginView
from users.apps import UsersConfig
from users.views import PhoneNumberCode, PhoneNumberCodesCode, PhoneNumberSomeoneInvite, PhoneNumberList, logout_view

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name='users/login.html'),name='login'),
    path("logout/", logout_view,name='logout'),
    path("home/", PhoneNumberList.as_view(), name="home"),
    path("", PhoneNumberCode.as_view(), name="phone"),
    path("phone_number/code/", PhoneNumberCodesCode.as_view(), name="code"),
    path("phone_number/code/invite/", PhoneNumberSomeoneInvite.as_view(), name="invite"),
    ]
