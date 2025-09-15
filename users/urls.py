from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    UpdateProfileView,
    ChangePasswordView,
    LogoutView,
    VerifyEmailView,
    #VerifyPhoneView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", UpdateProfileView.as_view(), name="profile-update"),
    path("profile/change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    #path("verify-phone/", VerifyPhoneView.as_view(), name="verify-phone"),

]
