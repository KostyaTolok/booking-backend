import logging
from typing import Any, Dict

import emails
from emails.template import JinjaTemplate

from config import config


def send_email(
    email_to: str,
    environment: Dict[str, Any],
    subject_template: str = "",
    html_template: str = "",
) -> None:
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(config.EMAILS_FROM_NAME, config.EMAILS_FROM_EMAIL),
    )
    logging.debug(message.as_string())


    # smtp_options = {"host": config.SMTP_HOST, "port": config.SMTP_PORT}
    # if config.SMTP_TLS:
    #     smtp_options["tls"] = True
    # if config.SMTP_USER:
    #     smtp_options["user"] = config.SMTP_USER
    # if config.SMTP_PASSWORD:
    #     smtp_options["password"] = config.SMTP_PASSWORD
    # response = message.send(to=email_to, render=environment, smtp=smtp_options)
    # logging.info(f"send email result: {response}")
