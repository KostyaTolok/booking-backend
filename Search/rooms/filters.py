import django_filters
from django_filters import rest_framework as filters

EQUIPMENT_STATES = {
    (0, "Pending_verification"),
    (1, "Verified"),
    (2, "Pending_equipment"),
    (3, "Equipment_installed")
}


class RoomFilter(django_filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    price = filters.RangeFilter()
    beds_number = filters.NumberFilter()
    has_washing_machine = filters.BooleanFilter()
    has_kitchen = filters.BooleanFilter()
    equipment_state = filters.ChoiceFilter(choices=EQUIPMENT_STATES)
    hotel = filters.NumberFilter()
    order = filters.OrderingFilter(
        fields=(
            ('price', 'price')
        )
    )

