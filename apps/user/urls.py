from django.urls import path, include

from rest_framework_simplejwt import views as jwt_views

from apps.user import views


urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name="login"),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name="login_refresh"),

    path('registration/', views.RegistrationAPIView.as_view(), name="sign_up"),
    path('registration/extra-info-mentor/', views.ExtraInfoMentorAPIView.as_view(), name="extra_info_mentor"),

    path('reset-password/', views.EmailPasswordResetAPIView.as_view(), name="reset_password"),
    path('reset-password/<uidb64>/<token>/',
         views.PasswordResetConfirmAPIView.as_view(), name="reset_password_confirm"),
]
