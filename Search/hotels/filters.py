import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q, Min


class HotelFilter(django_filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    address = filters.CharFilter(lookup_expr="icontains")
    has_parking = filters.BooleanFilter()
    has_wifi = filters.BooleanFilter()
    has_washing_machine = filters.BooleanFilter(field_name="rooms__has_washing_machine", distinct=True)
    has_kitchen = filters.BooleanFilter(field_name="rooms__has_kitchen", distinct=True)
    price = filters.RangeFilter(method="filter_price_range", distinct=True)
    owner = filters.NumberFilter()
    city = filters.NumberFilter()
    beds_number = filters.NumberFilter(field_name="rooms__beds_number", lookup_expr="gte", distinct=True)
    rooms_number = filters.NumberFilter(field_name="rooms__rooms_number", lookup_expr="gte", distinct=True)
    start_date = filters.DateFilter(method="filter_start_date")
    end_date = filters.DateFilter(method="filter_end_date")

    order = filters.OrderingFilter(
        fields=(
            ('rating', 'rating'),
            ('min_price', 'min_price'),
        ),
        distinct=True,
    )

    def filter_price_range(self, queryset, name, value):
        return queryset.filter(rooms__price__gte=value.start, rooms__price__lte=value.stop).annotate(
            min_price=Min("rooms__price")
        )

    def filter_start_date(self, queryset, name, value):
        return queryset.filter(
            Q(rooms__bookings__start_date__gt=value)
            | Q(rooms__bookings__end_date__lt=value)
            | Q(rooms__bookings__start_date=None)
        ).distinct()

    def filter_end_date(self, queryset, name, value):
        return queryset.filter(
            Q(rooms__bookings__start_date__gt=value)
            | Q(rooms__bookings__end_date__lt=value)
            | Q(rooms__bookings__end_date=None)
        ).distinct()
