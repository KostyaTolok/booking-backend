import logging
from typing import Union

import boto3


ses = boto3.client('ses')


def send_email(
        sender: str,
        recipients: Union[list, tuple],
        subject: str = "",
        html: str = "",
        text: str = "",
) -> None:
    message = {
        "Source": sender,
        "Destination": {'ToAddresses': recipients},
        "Message": {
            'Subject': {'Data': subject},
            'Body': {
                'Text': {'Data': text},
            }
        }
    }
    ses.send_email(**message)
    logging.info(message)
