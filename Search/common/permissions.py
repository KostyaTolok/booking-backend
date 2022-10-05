import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

from common.choices import Roles


class JWTBasePermission(BasePermission):
    def get_jwt_token(self, request):
        return request.headers.get("Authorization", None)

    def decode_token(self, request):
        jwt_token = self.get_jwt_token(request)

        if not jwt_token:
            raise AuthenticationFailed("Authentication token not provided")

        try:
            return jwt.decode(jwt_token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Authentication token has expired")
        except (jwt.DecodeError, jwt.InvalidTokenError):
            raise AuthenticationFailed("Authorization has failed, token is invalid")
        except Exception as e:
            raise AuthenticationFailed("Authorization has failed")

    def get_user_id(self, request):
        payload = self.decode_token(request)
        user_id = payload.get("sub")

        if not user_id:
            raise AuthenticationFailed("User id not provided")

        if not user_id.isdigit():
            raise AuthenticationFailed("User id is incorrect")


class IsAuthenticated(JWTBasePermission):
    def has_permission(self, request, view):
        self.decode_token(request)
        return True


class IsAdmin(JWTBasePermission):
    def has_permission(self, request, view):
        payload = self.decode_token(request)
        role = payload.get("role", None)
        return role == Roles.ADMIN.value
