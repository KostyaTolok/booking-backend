from functools import lru_cache

import boto3

from .config import config


@lru_cache
def get_resource(client_name):
    return boto3.resource(
        client_name,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION_NAME,
    )
