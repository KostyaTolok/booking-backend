import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.files.storage import Storage


class S3Storage(Storage):
    def __init__(self):
        assert hasattr(
            settings, "AWS_S3_BUCKET_NAME"
        ), "AWS_STORAGE_BUCKET_NAME is not set "
        self.bucket_name = settings.AWS_S3_BUCKET_NAME
        self.expiration_time = getattr(settings, "AWS_S3_URL_EXPIRATION_TIME", 3600)
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

    def save(self, name, content, max_length=None):
        self.client.put_object(Bucket=self.bucket_name, Key=name, Body=content)
        return name

    def url(self, name):
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": name},
            ExpiresIn=self.expiration_time,
        )

    def delete(self, name):
        self.client.delete_object(Bucket=self.bucket_name, Key=name)

    def exists(self, name):
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=name)
            return True
        except ClientError as e:
            if e.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                return False
            raise

    def size(self, name):
        response = self.client.head_object(Bucket=self.bucket_name, Key=name)
        return response["ContentLength"]
