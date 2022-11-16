from app.core.utils.email import send_email
from app.core.config import config


async def send_reset_password_email(email: str, token: str) -> None:
    message = {
        "email": email,
        "subject": "",
        "html": f"""
        <style>
            .button {{
              background-color: #E6A064;
              border-radius: 5px;
              color: white;
              padding: .5em;
              text-decoration: none;
            }}
        </style>
        <h2>PandaHouse password reset</h2>
        <p>
            Hi! We heard that you lost your PandaHouse password. Sorry about that!
        </p>
        <a class="button" href="https://{config.HOST}/booking-mobile/reset-password/confirm/{token}">Reset Your Password</a>
        """,
    }
    await send_email(**message)


async def send_confirm_email(email: str, code: str) -> None:
    message = {
        "email": email,
        "subject": "",
        "text": code,
    }
    await send_email(**message)
