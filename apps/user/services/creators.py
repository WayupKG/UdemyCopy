from django.contrib.auth import get_user_model

from .constants import ADMIN, MENTOR, USER

User = get_user_model()


def create_user(**data: dict[str, str]) -> User:
    """Создает пользователя по соответствующему категориям"""
    if data.get('user_type') == ADMIN:
        return User.objects.create_superuser(**data)
    elif data.get('user_type') == MENTOR:
        return User.objects.create_mentor(**data)
    elif data.get('user_type') == USER:
        return User.objects.create_user(**data)
