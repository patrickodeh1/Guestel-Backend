from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone",
            "first_name",
            "last_name",
            "password",
            "password2",
            "user_type",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2", None)
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        token = user.generate_verification_token()
        verification_url = f"http://localhost:8000/verify-email/{token}/"
        send_mail(
            subject="Verify Your Email",
            message=f"Click to verify: {verification_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        """ # Send phone OTP
        otp = user.generate_phone_otp()
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f"Your verification code is {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=user.phone
        )"""
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "user_type",
            "is_email_verified",
            "is_phone_verified",
            "is_identity_verified",
        )
        read_only_fields = (
            "first_name",
            "last_name",
            "is_email_verified",
            "is_phone_verified",
            "is_identity_verified",
        )

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone",)

    def update(self, instance, validated_data):
        if "phone" in validated_data and validated_data["phone"] != instance.phone:
            instance.is_phone_verified = False
        return super().update(instance, validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "New passwords do not match"})
        return attrs