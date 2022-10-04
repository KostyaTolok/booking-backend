from pydantic import BaseModel
from pydantic.networks import EmailStr

from app.core.utils.pydantic_extensions import PasswordStr


class Login(BaseModel):
    email: EmailStr
    password: str


class Reset(BaseModel):
    token: str
    new_password: PasswordStr
