from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegistrationSerializer


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegistrationSerializer
