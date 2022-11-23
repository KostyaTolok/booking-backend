import os
from uuid import uuid4

from django.conf import settings
from drf_yasg.generators import OpenAPISchemaGenerator


def path_and_rename(instance, filename, path):
    _, extension = os.path.splitext(filename)
    filename = f"{uuid4().hex}{extension}"
    return os.path.join(path, filename)


class SearchOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)
        schema.basePath = settings.SWAGGER_BASE_URL
        return schema
