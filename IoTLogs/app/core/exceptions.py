from http import HTTPStatus


class CustomException(Exception):
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    message = HTTPStatus.INTERNAL_SERVER_ERROR.description

    def __init__(self, message=None):
        if message:
            self.message = message
