from django.urls import path, include

from rest_framework_simplejwt import views as jwt_view

from apps.user import views


urlpatterns = [
    path('token/', jwt_view.TokenObtainPairView.as_view()),
    path('token/refresh/', jwt_view.TokenRefreshView.as_view()),
    path('sign-up/', views.RegistrationAPIView.as_view()),
    path('extra-info-mentor/', views.ExtraInfoMentorView.as_view()),
]
