from django.core.exceptions import ImproperlyConfigured
from django.views.generic.detail import SingleObjectMixin


class SerializerPermissionsMixin:

    def get_serializer_class(self):
        if self.serializer_classes is None:
            raise ImproperlyConfigured("Serializers are not set")

        default_serializer = self.serializer_classes.get('default')

        if not default_serializer:
            raise ImproperlyConfigured("Default serializer is not set")

        return self.serializer_classes.get(self.action, default_serializer)

    def get_permissions(self):
        if self.permission_classes is None:
            raise ImproperlyConfigured("Permissions are not set")

        default_permissions = self.permission_classes.get('default')

        if not default_permissions:
            raise ImproperlyConfigured("Default permissions are not set")

        return (permission() for permission in self.permission_classes.get(self.action, default_permissions))
