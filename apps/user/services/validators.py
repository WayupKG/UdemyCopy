from rest_framework.serializers import ValidationError


def validate_password(**data: dict[str, str]) -> dict[str, str]:
    if data.get('password') != data.get('password_confirm'):
        raise ValidationError(
            {"password_confirm": "Пароли не совпадают"}
        )
    data.pop('password_confirm')
    return data
