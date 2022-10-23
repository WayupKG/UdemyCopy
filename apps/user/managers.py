from typing import Any, Dict

from django.db import models
from django.contrib.auth.base_user import BaseUserManager

from .services.constants import ADMIN, MENTOR, USER


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields: Dict[str, Any]):
        """Создает и сохраняет пользователя с введенным им email и паролем."""
        if not email:
            raise ValueError('email должен быть указан')
        email = self.normalize_email(email.lower())
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str = None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('user_type', USER)
        return self._create_user(email, password, **extra_fields)

    def create_mentor(self, email: str, password: str = None, **extra_fields):
        extra_fields.setdefault('is_mentor', True)
        extra_fields.setdefault('user_type', MENTOR)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('user_type', ADMIN)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        return self._create_user(email, password, **extra_fields)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).order_by('-created_at')