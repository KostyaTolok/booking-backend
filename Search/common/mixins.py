from django.views.generic.detail import SingleObjectMixin


class SerializerPermissionsMixin(SingleObjectMixin):

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return (permission() for permission in
                self.permission_classes.get(self.action, self.default_permission_classes))
