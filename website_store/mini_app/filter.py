import django_filters
from mini_app.models import Product


class ProductSearch(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Цена от',
        required=False,
    )
    price__lt = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Цена до',
        required=False,
    )

    brand = django_filters.CharFilter(field_name='brand__brand',
                                      lookup_expr='iexact')

    cooling_power = django_filters.NumberFilter()
    cooling_power__gt = django_filters.NumberFilter(field_name='cooling_power',
                                                    lookup_expr='gte')
    cooling_power__lt = django_filters.NumberFilter(field_name='cooling_power'
                                                    , lookup_expr='lte')

    heating_power = django_filters.NumberFilter()
    heating_power__gt = django_filters.NumberFilter(field_name='heating_power',
                                                    lookup_expr='gte')
    heating_power__lt = django_filters.NumberFilter(field_name='heating_power',
                                                    lookup_expr='lte')

    working_area = django_filters.NumberFilter()
    working_area__gt = django_filters.NumberFilter(field_name='working_area',
                                                   lookup_expr='gte')
    working_area__lt = django_filters.NumberFilter(field_name='working_area', lookup_expr='lte')

    sound_level = django_filters.NumberFilter()
    sound_level__gt = django_filters.NumberFilter(field_name='sound_level',
                                                  lookup_expr='gte')
    sound_level__lt = django_filters.NumberFilter(field_name='sound_level',
                                                  lookup_expr='lte')

    country = django_filters.CharFilter(field_name='country__country',
                                        lookup_expr='iexact')

    view_main_menu = django_filters.BooleanFilter(field_name='view_main_menu')

    class Meta:
        model = Product
        fields = []
