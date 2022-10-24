from typing import Any

from rest_framework.serializers import ValidationError

from django.contrib.auth import get_user_model

User = get_user_model()


def validate_password(**data: dict[str, Any]) -> dict[str, Any]:
    if data.get('password') != data.pop('password_confirm'):
        raise ValidationError(
            {"password_confirm": "Пароли не совпадают"}
        )
    return data


def validate_user_email(email: str):
    user = User.objects.filter(email=email).exists()
    if not user:
        raise ValidationError(
            {"email": "Пользователь таким email'ом не найдено"}
        )
    return True
