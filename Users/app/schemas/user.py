from typing import Optional

from pydantic import BaseModel, EmailStr

from app.core.utils.pydantic_extensions import PasswordStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: PasswordStr


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[PasswordStr] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
