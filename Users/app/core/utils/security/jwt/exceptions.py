from http import HTTPStatus

from app.core.exceptions import CustomException


class InvalidToken(CustomException):
    code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    message = "Invalid token"
