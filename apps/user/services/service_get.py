import jwt

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import ValidationError


User = get_user_model()


def get_user_from_token(access_token: str) -> User:
    token = access_token.split(' ')[-1]
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    user_id = int(payload.get("user_id"))
    return User.objects.get(id=user_id)


def get_user_from_uidb64(uidb64: str) -> User:
    try:
        uid: str = force_str(urlsafe_base64_decode(uidb64))
        user: User = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        raise ValidationError({'uid': ['Invalid value']})
    return user