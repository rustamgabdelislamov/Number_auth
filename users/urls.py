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
    AddInviteView,
    AddInviteAPIView,
    MyProfileAPIView,
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
    path(
        "phone_number/code/invite_update/",
        AddInviteView.as_view(),
        name="invite_update",
    ),
    path("api/phone_number/", PhoneNumberCodeAPIView.as_view(), name="api_phone"),
    path(
        "api/phone_number/code/", PhoneNumberCodesCodeAPIView.as_view(), name="api_code"
    ),
    path(
        "api/phone_number/code/invite/",
        PhoneNumberSomeoneInviteAPI.as_view(),
        name="api_invite",
    ),
    path(
        "api/phone_number/code/invite_update/",
        AddInviteAPIView.as_view(),
        name="api_invite_update",
    ),
    path("api/", PhoneNumberListAPI.as_view(), name="api_home"),
    path("api/profile/", MyProfileAPIView.as_view(), name="api_profile"),
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
