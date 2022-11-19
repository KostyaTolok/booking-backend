from app.core.utils.email import send_email, render_template
from app.core.config import config


async def send_reset_password_email(email: str, token: str) -> None:
    message = {
        "email": email,
        "subject": "PandaHouse password reset",
        "html": render_template(
            "reset-password-email.html", host=config.HOST, token=token
        ),
    }
    await send_email(**message)


async def send_confirm_email(email: str, code: str) -> None:
    message = {
        "email": email,
        "subject": "",
        "text": code,
    }
    await send_email(**message)
