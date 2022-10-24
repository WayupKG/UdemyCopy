from typing import Any

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .permissions import AllowMentor
from .serializers import (
    RegistrationSerializer, ExtraInfoMentorSerializer,
    EmailSerializer, PasswordResetSerializer
)
from .services.service_get import get_user_from_token, get_user_from_uidb64

User = get_user_model()


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegistrationSerializer


class ExtraInfoMentorAPIView(CreateAPIView):
    permission_classes = [AllowMentor]
    serializer_class = ExtraInfoMentorSerializer

    def perform_create(self, serializer):
        serializer.save(
            mentor=get_user_from_token(self.request.headers.get('authorization'))
        )


class EmailPasswordResetAPIView(APIView):

    def post(self, *args: tuple[Any], **kwargs: dict[str: Any]) -> Response:
        serializer = EmailSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_email(
                protocol=self.request.META['wsgi.url_scheme'],
                domain=get_current_site(self.request).domain
            )
        return Response(
            {"detail": "Отправлено электронное письмо для сброса пароля."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmAPIView(UpdateAPIView):
    serializer_class = PasswordResetSerializer

    def get_object(self, **kwargs: dict[str: Any]) -> User:
        return get_user_from_uidb64(kwargs.get('uidb64'))

    def update(self, *args, **kwargs: dict[str: Any]) -> Response:
        user, data = self.get_object(**kwargs), self.request.data.dict()
        data.update({'uidb64': kwargs.get('uidb64'), 'token': kwargs.get('token')})

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=user, validated_data=serializer.validated_data)

        return Response(
            {"detail": "Пароль был сброшен с помощью нового пароля."},
            status=status.HTTP_200_OK
        )
