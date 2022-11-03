from app.core.utils.email import send_email


async def send_reset_password_email(email: str, token: str) -> None:
    message = {
        "email": email,
        "subject": "",
        "text": f"booking-mobile:///reset-password/confirm/{token}",
    }
    await send_email(**message)


async def send_confirm_email(email: str, code: str) -> None:
    message = {
        "email": email,
        "subject": "",
        "text": code,
    }
    await send_email(**message)
