import jwt

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def get_user(access_token: str) -> User:
    token = access_token.split(' ')[-1]
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    user_id = int(payload.get("user_id"))
    return User.objects.get(id=user_id)
