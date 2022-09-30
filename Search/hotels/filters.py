import django_filters
from django_filters import rest_framework as filters


class HotelFilter(django_filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    address = filters.CharFilter(lookup_expr="icontains")
    has_parking = filters.BooleanFilter()
    has_wifi = filters.BooleanFilter()
    has_washing_machine = filters.BooleanFilter(field_name="rooms__has_washing_machine")
    has_kitchen = filters.BooleanFilter(field_name="rooms__has_kitchen")
    price = filters.RangeFilter(field_name="rooms__price")
    owner = filters.NumberFilter()
    beds_number = filters.NumberFilter(field_name="rooms__beds_number", lookup_expr="gte")
    order = filters.OrderingFilter(
        fields=(
            ('rating', 'rating'),
            ('rooms__price', "price")
        )
    )
