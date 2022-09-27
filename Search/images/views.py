from rest_framework import mixins, viewsets

from images.models import Image
from images.serializers import ImageSerializer


class ImagesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
