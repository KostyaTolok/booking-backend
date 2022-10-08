import re


class PasswordStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: str) -> str:
        if len(value) < 10:
            raise ValueError("password must be at lest 10 letters")

        rx = re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{10,}$")
        if not rx.match(value):
            raise ValueError(
                "password must include at least digit number, an uppercase and a lowercase letter"
            )

        return value
