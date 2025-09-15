from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import AnonRateThrottle


from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    UpdateProfileSerializer,
    ChangePasswordSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    throttle_classes = [AnonRateThrottle]
    throttle_scope = 'login'

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        identifier = request.data.get("identifier")
        password = request.data.get("password")
        
        if not identifier or not password:
            return Response(
                {"error": "Identifier and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, identifier=identifier, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"old_password": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"detail": "Password updated successfully"})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out"})
        except Exception:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        try:
            user = User.objects.get(email_verification_token=token)
            if user.is_email_verified:
                return Response({"detail": "Email already verified"}, status=status.HTTP_400_BAD_REQUEST)
            user.is_email_verified = True
            user.email_verification_token = None
            user.save()
            return Response({"detail": "Email verified successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


"""class VerifyPhoneView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        otp = request.data.get("otp")
        try:
            user = User.objects.get(phone=phone, phone_verification_token=otp)
            if user.is_phone_verified:
                return Response({"detail": "Phone already verified"}, status=status.HTTP_400_BAD_REQUEST)
            user.is_phone_verified = True
            user.phone_verification_token = None
            user.save()
            return Response({"detail": "Phone verified successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid phone or OTP"}, status=status.HTTP_400_BAD_REQUEST)
            """