import django_filters
from django_filters import rest_framework as filters


class HotelFilter(django_filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    address = filters.CharFilter(lookup_expr="icontains")
    has_parking = filters.BooleanFilter()
    has_wifi = filters.BooleanFilter()
    price = filters.RangeFilter(field_name="rooms__price")
    owner = filters.NumberFilter()
    order = filters.OrderingFilter(
        fields=(
            ('rating', 'rating'),
            ('rooms__price', "price")
        )
    )
