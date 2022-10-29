from django.test import TestCase
from django.urls import resolve, reverse

from rest_framework_simplejwt import views as jwt_views

from apps.user import views


class TestUrls(TestCase):
    """Тестирование url адресы"""

    def test_login(self):
        url = reverse('login')
        view_class = resolve(url).func.view_class
        return self.assertEqual(view_class, jwt_views.TokenObtainPairView)

    def test_login_refresh(self):
        url = reverse('login_refresh')
        view_class = resolve(url).func.view_class
        return self.assertEqual(view_class, jwt_views.TokenRefreshView)

    def test_sign_up(self):
        url = reverse('registration')
        view_class = resolve(url).func.view_class
        return self.assertEqual(view_class, views.RegistrationAPIView)

    def test_extra_info_mentor(self):
        url = reverse('extra_info_mentor')
        view_class = resolve(url).func.view_class
        return self.assertEqual(view_class, views.ExtraInfoMentorAPIView)

    def test_reset_password(self):
        url = reverse('reset_password')
        view_class = resolve(url).func.view_class
        return self.assertEqual(view_class, views.EmailPasswordResetAPIView)

    def test_reset_password_confirm(self):
        url = reverse('reset_password_confirm', args=["Mg", "bdtsfv-e732384f23caf82fa2cd2251f4e59105"])
        view_class = resolve(url).func.view_class
        return self.assertEqual(view_class, views.PasswordResetConfirmAPIView)
