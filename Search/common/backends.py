import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        request.user = None
        jwt_token = request.headers.get("Authorization", None)

        if not jwt_token:
            return None, None

        payload = self.decode_token(jwt_token)

        self.check_active_status(payload)

        user = {"user_id": self.get_user_id(payload), "role": self.get_role(payload)}

        return user, jwt_token

    def decode_token(self, jwt_token):
        try:
            return jwt.decode(jwt_token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Authentication token has expired")
        except (jwt.DecodeError, jwt.InvalidTokenError):
            raise AuthenticationFailed("Authorization has failed, token is invalid")
        except Exception as e:
            raise AuthenticationFailed("Authorization has failed")

    def get_user_id(self, payload):
        user_id = payload.get("sub")

        if user_id is None:
            raise AuthenticationFailed("User id not provided")

        if not user_id.isdigit():
            raise AuthenticationFailed("User id is incorrect")

        return int(user_id)

    def get_role(self, payload):
        role = payload.get("role")

        if role is None:
            raise AuthenticationFailed("User role is not provided")

        return role

    def check_active_status(self, payload):
        is_active = payload.get("active")

        if is_active is None:
            raise AuthenticationFailed("User active status is not provided")

        if not is_active:
            raise AuthenticationFailed("User is inactive")
