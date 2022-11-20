import logging
from typing import Union

import boto3


ses = boto3.client("ses")


def send_email(
    sender: str,
    recipients: Union[list, tuple],
    subject: str = "",
    html: str = None,
    text: str = None,
) -> None:
    message = {
        "Source": sender,
        "Destination": {"ToAddresses": recipients},
        "Message": {
            "Subject": {"Data": subject},
        },
    }
    if html:
        message["Message"]["Body"] = {"Html": {"Data": html}}
    elif text:
        message["Message"]["Body"] = {"Text": {"Data": text}}
    ses.send_email(**message)
    logging.info(message)
