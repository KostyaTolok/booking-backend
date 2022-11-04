from app.core.utils.email import send_email
from app.core.config import config


async def send_reset_password_email(email: str, token: str) -> None:
    message = {
        "email": email,
        "subject": "",
        "text": f"{config.MOBILE_URL_SCHEMA}:///reset-password/confirm/{token}",
    }
    await send_email(**message)


async def send_confirm_email(email: str, code: str) -> None:
    message = {
        "email": email,
        "subject": "",
        "text": code,
    }
    await send_email(**message)
