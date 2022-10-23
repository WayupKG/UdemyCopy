from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from .permissions import AllowMentor
from .serializers import RegistrationSerializer, ExtraInfoMentorSerializer
from .services.service_get import get_user


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegistrationSerializer


class ExtraInfoMentorView(CreateAPIView):
    permission_classes = [AllowMentor]
    serializer_class = ExtraInfoMentorSerializer

    def perform_create(self, serializer):
        serializer.save(
            mentor=get_user(self.request.headers.get('authorization'))
        )