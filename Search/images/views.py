from rest_framework import mixins, viewsets

from images.models import Image
from images.serializers import ImageSerializer
from search.permissions import IsAdmin


class ImagesViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ImageSerializer
    permission_classes = (IsAdmin,)
    queryset = Image.objects.all()

