import django_filters
from django_filters import rest_framework as filters

from common.choices import EquipmentStates


class RoomFilter(django_filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    price = filters.RangeFilter()
    beds_number = filters.NumberFilter(lookup_expr="gte")
    has_washing_machine = filters.BooleanFilter()
    has_kitchen = filters.BooleanFilter()
    equipment_state = filters.ChoiceFilter(choices=EquipmentStates.choices)
    hotel = filters.NumberFilter()
    order = filters.OrderingFilter(
        fields=(('price', 'price'),),
    )
