from django.urls import path, include

from apps.user import views


urlpatterns = [
    path('sign-up/', views.RegistrationAPIView.as_view()),
]
