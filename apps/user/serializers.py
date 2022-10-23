from typing import Any

from rest_framework import serializers

from django.contrib.auth import get_user_model

from .services.constants import ADMIN, MENTOR, USER
from .services.validators import validate_password
from .services.creators import create_user

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
