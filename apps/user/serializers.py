from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .models import ExtraInfoMentor
from .services.tokens import password_reset_token
from .services.validators import validate_password, validate_user_email
from .services.creators import create_user
from .tasks import reset_password_email_send

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализация регистрации пользователя"""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'sur_name', 'user_type', 'password', 'password_confirm']

    def validate(self, validated_data: dict[str, str]) -> dict[str, str]:
        to_validate = validate_password(**validated_data)
        return to_validate

    def create(self, validated_data):
        """Определить пользователя и создать"""
        return create_user(**validated_data)


class ExtraInfoMentorSerializer(serializers.ModelSerializer):
    """Сериализация дополнительной информации наставника"""

    class Meta:
        model = ExtraInfoMentor
        fields = ['type_of_experience', 'audience']


class EmailSerializer(serializers.Serializer):
    """Сериализация email для отправки писем на почту"""
    email = serializers.EmailField()

    def validate(self, validated_data: dict[str, str]) -> dict[str, str]:
        validate_user_email(validated_data.get('email'))
        return validated_data

    def send_email(self, *, protocol: str, domain: str):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = password_reset_token.make_token(user)
        reset_password_email_send.delay(
            email=email, full_name=user.get_full_name(),
            protocol=protocol, domain=domain,
            uid=uid, token=token
        )


class PasswordResetSerializer(serializers.Serializer):
    """Сериализация для сброса пароля"""
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=128, min_length=8, write_only=True)

    def validate(self, validated_data: dict[str, str]) -> dict[str, str]:
        return validate_password(**validated_data)

    def update(self, instance, validated_data):
        if password_reset_token.check_token(instance, validated_data.get('token')):
            instance.set_password(validated_data.get('password'))
            instance.save()
            return instance
        raise ValidationError({"detail": "Ссылка для сброса пароля недействительна."})
