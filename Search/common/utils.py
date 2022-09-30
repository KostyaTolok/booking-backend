import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


def decode_token(jwt_token):
    try:
        return jwt.decode(jwt_token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Authentication token has expired")
    except (jwt.DecodeError, jwt.InvalidTokenError):
        raise AuthenticationFailed("Authorization has failed, token is invalid")
    except Exception as e:
        raise AuthenticationFailed("Authorization has failed")
