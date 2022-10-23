from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from apps.user.managers import UserManager, ActiveManager
from .services.constants import ADMIN, MENTOR, USER


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь"""

    USER_TYPE = (
        (ADMIN, 'Admin'),
        (MENTOR, 'Mentor'),
        (USER, 'User'),
    )

    username = None
    email = models.EmailField('email', unique=True)
    last_name = models.CharField('Фамилия', max_length=40)
    first_name = models.CharField('Имя', max_length=40)
    sur_name = models.CharField('Отчество', max_length=50, blank=True, null=True)
    user_type = models.CharField('Тип пользователя', max_length=10, choices=USER_TYPE)

    is_superuser = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    reset_password = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    active = ActiveManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'sur_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self) -> str:
        """Возвращает first_name, last_name и part_name с пробелом между ними."""
        if self.sur_name:
            return f"{self.first_name} {self.last_name} {self.sur_name}".strip()
        return f"{self.first_name} {self.last_name}".strip()


class MentorInfo(models.Model):
    EXPERIENCE = (
        ('privately', 'лично, частным образом'),
        ('professionally', 'лично, профессионально'),
        ('online', 'онлайн'),
        ('other', 'другое'),
    )

    AUDIENCE = (
        ('not_moment', 'в настоящий момент нет'),
        ('small_audience', 'у меня маленькая аудитория'),
        ('sufficient_audience', 'у меня достаточная аудитория'),
    )

    mentor = models.OneToOneField(User, on_delete=models.CASCADE, related_name='questions')
    type_of_experience = models.CharField('Каким видом преподавания вы занимались раньше?',
                                          max_length=15, choices=EXPERIENCE)
    audience = models.CharField('Есть ли у вас аудитория, с которой вы хотите поделиться своим курсом?',
                                max_length=20, choices=AUDIENCE)


class Payment(models.Model):
    """Платеж"""
    status = models.CharField('status', max_length=11)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    amount = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self) -> str:
        return f"Платеж - {self.user}"