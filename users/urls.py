from django.urls import path
from django.contrib.auth.views import LoginView
from users.apps import UsersConfig
from users.views import (
    PhoneNumberCode,
    PhoneNumberCodesCode,
    PhoneNumberSomeoneInvite,
    PhoneNumberList,
    logout_view,
    PhoneNumberCodeAPIView,
    PhoneNumberCodesCodeAPIView,
    PhoneNumberSomeoneInviteAPI,
    PhoneNumberListAPI,
)
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", logout_view, name="logout"),
    path("", PhoneNumberList.as_view(), name="home"),
    path("phone_number/", PhoneNumberCode.as_view(), name="phone"),
    path("phone_number/code/", PhoneNumberCodesCode.as_view(), name="code"),
    path(
        "phone_number/code/invite/", PhoneNumberSomeoneInvite.as_view(), name="invite"
    ),
    path("api/phone_number/", PhoneNumberCodeAPIView.as_view(), name="api_phone"),
    path(
        "api/phone_number/code/", PhoneNumberCodesCodeAPIView.as_view(), name="api_code"
    ),
    path(
        "api/phone_number/code/invite/",
        PhoneNumberSomeoneInviteAPI.as_view(),
        name="api_code",
    ),
    path("api/", PhoneNumberListAPI.as_view(), name="api_home"),
    path(
        "api/login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="api_login",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="api_token_refresh",
    ),
]
