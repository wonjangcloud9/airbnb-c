import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class TrustMeBroAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print(request.headers)
        username = request.headers.get("Trust-Me")
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No user {username}")


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print(request.headers)
        token = request.headers.get("jwt")
        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            pk = payload.get("pk")
            user = User.objects.get(pk=pk)
            return (user, None)
        except jwt.exceptions.DecodeError:
            raise AuthenticationFailed("Token is invalid")
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No user {username}")
