from django.urls import path, include

from rest_framework_simplejwt import views as jwt_views

from apps.user import views


urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name="login"),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name="login_refresh"),

    path('sign-up/', views.RegistrationAPIView.as_view(), name="sign-up"),
    path('extra-info-mentor/', views.ExtraInfoMentorAPIView.as_view(), name="extra-info-mentor"),

    path('reset-password/', views.EmailPasswordResetAPIView.as_view(), name="reset-password"),
    path('reset-password-confirm/<uidb64>/<token>/',
         views.PasswordResetConfirmAPIView.as_view(), name="reset-password-confirm"),
]
