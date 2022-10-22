from collections import OrderedDict

from rest_framework_mongoengine import serializers

from search_requests.models import SearchRequest


class SearchRequestSerializer(serializers.DocumentSerializer):
    class Meta:
        model = SearchRequest

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation = OrderedDict([(key, value) for key, value in representation.items() if value is not None])
        return representation
