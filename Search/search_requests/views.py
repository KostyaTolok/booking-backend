from rest_framework_mongoengine import viewsets, generics

from common.permissions import IsAuthenticated
from search_requests.models import SearchRequest
from search_requests.serializers import SearchRequestSerializer


class SearchRequestsViewSet(
    generics.mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SearchRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.get("user_id")
        return SearchRequest.objects.filter(user=user_id).order_by("-created_at")[:10]
