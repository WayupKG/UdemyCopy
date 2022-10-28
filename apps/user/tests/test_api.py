from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import resolve, reverse

from apps.user.serializers import RegistrationSerializer


class TestRegistrationAPI(APITestCase):
    """Тестирование регистрации"""

    def test_sign_up(self):
        payload = {
            'email': 'adiTest@mail.ru',
            'first_name': 'Adi',
            'last_name': 'Test',
            'user_type': 'admin',
            'password': '123456789',
            'password_confirm': '123456789',
        }
        url = reverse('sign-up')
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
