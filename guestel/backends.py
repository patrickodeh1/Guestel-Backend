from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, identifier=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(phone=identifier)
            except User.DoesNotExist:
                return None

        if user and user.check_password(password):
            return user
        return None