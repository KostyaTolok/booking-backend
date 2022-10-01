from django.views.generic.detail import SingleObjectMixin


class SerializerPermissionsMixin(SingleObjectMixin):

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_classes.get('default'))

    def get_permissions(self):
        return (permission() for permission in
                self.permission_classes.get(self.action, self.permission_classes.get('default')))
