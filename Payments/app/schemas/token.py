from pydantic import BaseModel


class Token(BaseModel):
    jti: str
    exp: int
    sub: int
    type: str
    role: str
    active: bool
    email: str
