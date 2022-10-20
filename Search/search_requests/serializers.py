from rest_framework_mongoengine import serializers

from search_requests.models import SearchRequest
from search_requests.utils import search_request_params


class SearchRequestSerializer(serializers.DocumentSerializer):
    class Meta:
        model = SearchRequest
        fields = search_request_params
