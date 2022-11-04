from datetime import timedelta

from app import crud
from app.core.config import config
from app.core import exceptions
from app.core.utils.security import confirmation_code
from app.services.email import send_confirm_email, send_reset_password_email
from app.models import User
from app.core.utils.security.jwt import tokens
from app.services.user import UserService


class ConfirmService:
    @staticmethod
    async def send_recover_password_email(db, *, user: User):
        password_reset_token = tokens.RefreshToken(db).for_user(subject=user.id)
        password_reset_token.set_expiration(
            timedelta(hours=config.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
        )
        await send_reset_password_email(
            email=user.email, token=str(password_reset_token)
        )

    @staticmethod
    def reset_password(db, *, token: str, new_password: str) -> User:
        token = tokens.RefreshToken(db, token=token)
        token.blacklist()

        user = UserService.get_user(db, id=token["sub"])
        return UserService.update_user(
            db, db_obj=user, obj_in={"password": new_password}
        )

    @staticmethod
    async def send_email_confirmation_code(user: User):
        if user.is_active:
            raise exceptions.BadRequestException(message="Email is already confirmed")

        code = confirmation_code.get_code(subject=user.email)
        await send_confirm_email(email=user.email, code=code)

    @staticmethod
    async def confirm_email(db, *, user: User, code: str) -> User:
        if user.is_active:
            raise exceptions.BadRequestException(message="Email is already confirmed")

        if not confirmation_code.verify_code(subject=user.email, code=code):
            raise exceptions.ForbiddenException(
                message="Confirm code is invalid or expired"
            )

        return crud.user.update(db, db_obj=user, obj_in={"is_active": True})
