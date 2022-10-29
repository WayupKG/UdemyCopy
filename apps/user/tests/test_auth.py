from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestAuthAPI(APITestCase):
    """Тестирование аутентификации"""
    def setUp(self) -> None:
        self.payload_login = {
            'email': 'aditest@mail.ru',
            'password': '123456789',
        }
        self.payload = {
            'first_name': 'Adi',
            'last_name': 'Test',
            'user_type': 'admin'
        }
        self.payload.update(
            **self.payload_login,
            password_confirm=self.payload_login.get('password')
        )
        url = reverse('registration')
        self.response = self.client.post(url, data=self.payload)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_login_and_refresh(self):
        url = reverse('login')
        response = self.client.post(url, data=self.payload_login)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

        url_refresh = reverse('login_refresh')
        payload = {'refresh': response.data.get('refresh')}
        response2 = self.client.post(url_refresh, data=payload)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertIn('access', response2.data)


